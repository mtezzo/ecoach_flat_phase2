from tailoring2.render import tostring
from tailoring2.authorutil import isEmpty
from tailoring2.substitute import sub_variables
try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.new

from tailoring2.common import ET
from tailoring2 import render

from formatutils import command_iterator, parent_map, first_command_of_type
from formatutils import msgids_in_tree, enclosing_command_of_type
from formatutils import Bunch, WHOLE_CONTAINERS, make_factory
from formatutils import tree_has_content
from projectutils import data_to_dictionary_types, InvalidDataError
from slicing import ClassicSlicer
import operator

try:
    import bridging
except ImportError:
    pass

try:
    PageBase = bridging.PageBase
except (NameError, AttributeError):
    PageBase = object

try:
    SurveyManagerBase = bridging.SurveyManagerBase
except (NameError, AttributeError):
    SurveyManagerBase = object

try:
    SurveyStateBase = bridging.SurveyStateBase
except (NameError, AttributeError):
    SurveyStateBase = object

def first(iterable, default=None):
    try:
        return iter(iterable).next()
    except StopIteration:
        return default

class Condition(object):
    """A wrapper around a python expression for later testing on an object
    Additional metadata can be assigned to the condition for specific uses."""
    
    def __init__(self, condition, **kwargs):
        """Create a Condition based on an expression string, and any
        additional keyword arguments. All keyword args are assumed into the
        Condition's attribute dictionary, for easy access."""
        self.condition = condition
        self.__dict__.update(kwargs)
    
    def evaluate(self, context):
        """evaluate the Condition with context as the local namespace"""
        return eval(self.condition, dict(), context)
    
    def __hash__(self):
        return hash(self.condition)
    
    def __repr__(self):
        return "<%s: %r>" % ( self.__class__, self.condition )

class Page(PageBase):
    """A wraper for an element tree consisting of a discrete, displayable
    survey 'page'.  Given an ElementTree Element object, a Page will be
    created with the following attributes:
        - tree: the ElementTree Element root node.
        - characteristics: a set of all characteristic names assigned to a
            question command within the page.
        - names: a set of all names within the page.
        - id: a 40-char hexidecimal digest hash of all of the message-ids
            within the page, intended to be unique amaong all pages.
        - ids: a set of the message-ids for all commands within the page
    """
    
    def __init__(self, tree):
        self.tree = tree
        if not tree:
            tree.hello
            
        self.characteristics = set()
        self.names = set()        
        self.firstname = ''
        
        for command in command_iterator(tree):
            if 'characteristic' in command.attrib:
                self.characteristics.add(command.get('characteristic'))
            if 'name' in command.attrib:
                self.names.add(command.get('name'))
                if len(self.firstname) <= 0:
                    self.firstname = command.get('name')

            
#        self.characteristics = set(command.get('characteristic') for command
#            in command_iterator(tree) if 'characteristic' in command.attrib)
#        self.names = set(command.get('name') for command
#            in command_iterator(tree) if 'name' in command.attrib)
        self.parentage = parent_map(self.tree)
        ids = msgids_in_tree(tree)
        self.id = sha1(','.join(ids)).hexdigest()
        self.ids = set(ids)
    
    def __repr__(self):
        return '<Page %s>' % self.id
    
    def tree_without_conditions(self):
        """returns a copy of self.tree without any if attributes"""
        copier = make_factory(self.tree, None, None)
        new_tree = copier()
        for command in command_iterator(new_tree):
            if_ = command.get('if')
            if if_ is not None:
                del command.attrib['if']
        return new_tree
    
    def goto_commands(self):
        """returns a list of command Elements that have non-empty goto
        attributes in document order."""
        gotos = []
        for command in command_iterator(self.tree):
            goto = command.get('goto')
            if goto is not None and goto.strip() != '':
                gotos.append(command)
        return gotos
    
    def validate_commands(self):
        """returns a list of "validate" command Elements in document order."""
        validates = []
        for command in command_iterator(self.tree):
            if command.tag == 'validate':
                validates.append(command)
        return validates
    
    def _if_conditions_for(self, command):
        com_conds = []
        parent = command
        while parent is not None:
            if_ = parent.get('if')
            if if_ is not None:
                com_conds.append(if_)
            parent = self.parentage[parent]
        return com_conds
    
    def validation_conditions(self):
        """returns a list of Condition objects for each "validate" command
        within self.tree. Condition objects also contain a "validate_type"
        attribute which is either 'strict' or 'loose', depending on the
        underlying command."""
        conditions = []
        parentage = parent_map(self.tree)
        for command in self.validate_commands():
            validate_type = command.get('validatetype', 'strict')
            ifs = self._if_conditions_for(command)
            if len(ifs) == 0:
                ifs.append('True')
            condition = Condition('( %s )' % ') and ('.join(reversed(ifs)),
                validate_type=validate_type, command=command)
            conditions.append(condition)
        return conditions
    
    def goto_conditions(self):
        """returns a list of Condition objects for each command with a "goto"
        attribute within self.tree.  Conditions objects also contain a
        "destination" attribute which is a string."""
        conditions = []
        parentage = parent_map(self.tree)
        for command in self.goto_commands():
            ifs = self._if_conditions_for(command)
            if command.tag == 'response':
                question = enclosing_command_of_type(self.tree,
                    command, 'question')
                if question is not None:
                    ifs.append('str(%s) == %r' % ( question.get('characteristic'),
                                              command.get('value')))
            if command.tag == 'question':
                ifs.append('not isEmpty(%s)' % command.get('characteristic'))
            if len(ifs) == 0:
                ifs.append('True')
            condition = Condition('( %s )' % ') and ('.join(reversed(ifs)),
                destination=command.get('goto'), command=command)
            conditions.append(condition)
        return conditions
    
    def get_ids(self):
        return self.ids
    
    def get_id(self):
        return self.id
    
    def get_tree(self):
        return self.tree

    def get_xml(self):
        return render.tostring(self.tree)
    
    def get_names(self):
        return self.names
    
    def get_characteristics(self):
        return self.characteristics
    

class ValidationError(Exception):
    """A failure when a subject fails to pass the conditions of a validate
    command.
    Attributes:
        - failed_expression: the string of the expression that evaluated to
            True (a bit of a confusing name; the failure is when the
            expression evaluates to True, not False)
        - validate_type: 'strict' or 'loose', depending on the underlying
            command
    """
    def __init__(self, failed_expression, validate_type='strict'):
        self.failed_expression = failed_expression
        self.validate_type = validate_type
    
    def __str__(self):
        return "failed on %r (%s)" % (self.failed_expression, self.validate_type)
    

class GotoDestination(Exception):
    """A non-error exception raised if a Subject can pass a page (i.e. it
    satisfies all validation conditions), and a condition under which a user
    is forwarded to a new page is True.  SurveyState objects should never
    allow such an exception to escape the Survey Engine.
    Attributes:
        - page: the page object destination.
        - destination_name: the name of the command the condition points to
    """
    def __init__(self, page, destination_name=None):
        self.page = page
        self.destination_name = destination_name
    
    def __str__(self):
        return "Goto Page %r for %s" % ( self.page, self.destination_name )
    

class InsufficientDataError(Exception):
    """A more descriptive stand-in for a NameError within a logic evaluation.
    These will occur when a Subject does not contain any data for a name
    in a Condition."""
    pass

class EndOfSurvey(Exception):
    """A signaling exception for when the Engine has reached the end of all of
    the survey pages. 
    """
    pass

class SurveyManager(SurveyManagerBase):
    """A SurveyManager provides the structure for a single, complete Survey.
    It contains now shared state for any user's progress through a survey;
    that job is left to the SurveyStates.  Instead, it provides the structure
    for the SurveyStates to move through a Survey.
    Attributes:
        - pages: an ordered list of Page objects
        - project: a tailoring2 BasicProject, or subclass thereof.
        - source: a string representing the name of the source that incoming
            data will reside in. (default: the empty string)
    """
    def __init__(self, pages, project, source=None):
        self.pages = pages
        self.project = project
        self.source = source if source is not None else ''
    
    def page(self, number):
        """get the Page in the survey at position 'number', where the first
        page is page 1.  If the index is out of range, EndOfsurvey is
        raised."""
        try:
            return self.pages[number - 1]
        except IndexError:
            raise EndOfSurvey()
    
    def next_page(self, page):
        """get the Page immediately following page.  If page is the last page,
        EndOfSurvey is raised."""
        try:
            return self.pages[self.pages.index(page) + 1]
        except IndexError:
            raise EndOfSurvey()
    
    def find_goto_page(self, name):
        """get the Page containing the name within a command name."""
        for page in self.pages:
            if name in page.names:
                return page
        # the following loop is likely a bug-causing troublemaker
        # for page in self.pages:
        #     if name in page.characteristics:
        #         return page
        return None
    
    def next_page_for_context(self, page, context):
        """get the Page that the Subject (passed as an EvaluationContext)
        should advance to, given the state of that subject. If page is the
        last page, EndOfSurvey is raised."""
        flatcontext = context.flatdict()
        for condition in page.goto_conditions():
            if condition.evaluate(flatcontext):
                thedest = condition.destination
                try:
                    thedest = sub_variables(thedest, flatcontext)
                except Exception, e:
                    print e
                    pass
                return self.find_goto_page(thedest)
        return self.next_page(page)
    
    def can_pass_page(self, page, context, ignore_loose_validation=False):
        """Assert that with a given Subject (passed as an EvaluationContext,
        context) can successfully move on to the next page in the Survey.
        ignore_loose_validation can be set to allow loose validation failures
        to not prohibit forward progress.
        Returns None if page is None
        Returns True iff:
            - all validation conditions are False or are 'loose', and
                ignore_loose_validation is True
            - there are no goto conditions that are True
            - there are no NameErrors raised in the above.
        If there are no validation errors, but a goto condition is
        encountered, a GotoDestination exception is raised immediately. Any
        instance of a NameError is captured, and an InsufficientDataError
        is raised.
        """
        if page is None:
            return None
        try:
            flatcontext = context.flatdict()
            for condition in page.validation_conditions():
                if condition.validate_type == 'loose' and ignore_loose_validation:
                    continue                    
                if condition.evaluate(flatcontext):
                    raise ValidationError(condition, condition.validate_type)
            for condition in page.goto_conditions():
                if condition.evaluate(flatcontext):
                    thedest = condition.destination
                    try:
                        thedest = sub_variables(thedest, flatcontext)
                    except Exception, e:
                        print e
                        pass                    
                    raise GotoDestination(self.find_goto_page(thedest),
                        thedest)
        except NameError:
            raise InsufficientDataError()
        return True
    
    def page_with_id(self, id):
        """return the first Page in the Survey that has this id"""
        return first(p for p in self.pages if p.id == id)
    
    def first_page_with_msgid(self, msgid):
        """return the first Page in the Survey that contains id in its tree's
        command's message-ids.  If no page is found, return None."""
        return first(p for p in self.pages if msgid in p.ids)
    
    def unique_msgids_for_page(self, page):
        """return the set of msgids that is unique only to `page` among all of
        the manager's pages."""
        pages = list(self.pages)
        pages.remove(page)
        while page in pages: # a little defensive coding here
            pages.remove(page)
        pages.insert(0, page)
        return reduce(operator.sub, (p.ids for p in pages))
    
    def first_unique_msgid_for_page(self, page):
        """return a single msgid that is in the set of msgids unique only to
        `page` among all of the manager's pages."""
        return first(self.unique_msgids_for_page(page))
    
    def get_all_characteristics(self):
        """return a set of all unique characteristic names within all
        pages."""
        return reduce(operator.or_,
            (page.characteristics for page in self.pages))
    
    def get_pages(self):
        return self.pages
    
    def get_source(self):
        return self.source
    
    def set_source(self, source):
        self.source = source
    
    def get_project(self):
        return self.project

class SurveyState(SurveyStateBase):
    """A container for unique survey-related state management.  Some data is
    managed by the client, and some is mutated within SurveyState.
    Attributes:
        - manager: the SurveyManager instance the state belongs to
        - subject: tailoring2 Subject instance, managed by the calling
            application. Any updates to the state of the Subject is outside
            the perview of the SurveyState, although there is a helper to
            create one (subject_with_overlaid_data) and to update the current
            subject instance (update_current_subject).
        - current_page: Page instance the state is set to render and respond
            to. It is updated by this instance.
        - validation_errors: a counter for the number of times a submission
            has been made to current_page resulting in at least one
            ValidationError. It is updated by this instance.
    """
    def __init__(self, manager, subject):
        self.manager = manager
        self.subject = subject
        self.current_page = manager.pages[0]
        self.validation_errors = 0
    
    def update_current_subject(self, data):
        """Destrucitvely update self.subject with the results from
        self.subject_with_overlaid_data(data)."""
        tsub = self.subject_with_overlaid_data(data)
        if tsub == self.subject:
            return
        pc = self.subject.primary_chars
        sc = self.subject.selection_chars
        mc = self.subject.message_chars
        def copy_from_dict(d1, d2):
            d2.clear()
            for key in d1:
                d2[key] = d1[key]
        copy_from_dict(tsub.primary_chars, pc)
        copy_from_dict(tsub.selection_chars, sc)
        copy_from_dict(tsub.message_chars, mc)
    
    def subject_with_overlaid_data(self, data):
        """Given a set of non-sourced input data, returns a tailoring2 Subject
        instance that is based on that created by merging the new data with
        self.subject.  The non-sourced data will be assigned placed in
        self.manager.source after the data is coerced to the project's
        dictionary types.  The derived machinery will have been run."""
        if not data:
            return self.subject
        data = data_to_dictionary_types(data, self.manager.project.mtsdict)
        primary_chars = dict((key, dict(val)) for key, val in
            self.subject.primary_chars.items())
        if self.manager.source not in primary_chars:
            primary_chars[self.manager.source] = dict()
        primary_chars[self.manager.source].update(data)
        sfpc = self.manager.project.subject_for_primary_chars
        return sfpc(primary_chars)[0]
    
    def render(self, data={}, show_errors=None, treq=None):
        """Run a tailoring2 Pipeline for the given subject on current_page.
        All parameters are optional:
        - data: a flat, unsourced dictionary-like object containing any
            additional data (form submission fields) that should be added to
            the subject before running the pipeline. The values will be
            coerced to dictionary types, and placed in self.manager.source (or
            treq.default_source, if present), before being overlaid above
            self.subject.
        - show_errors: True if the output should contain content from validate
            commands. This will override treq.show_errors if it is not None.
        - treq: a tailoring2 tailoring request. Relevant attributes for
            render() on the treq are:
            - show_errors: (as above)
            - default_source: overrides self.manager.source for this run of
                the pipeline.
        The result will be the same as calling tailoring2.Pipeline.run(), a
        tuple containing a result ElementTree, ready for serialization, and a
        python list of tailoring2 errors.
        """
        if treq is None:
            treq = Bunch(default_source=self.manager.source)
        if not hasattr(treq, 'default_source'):
            treq.default_source = self.manager.source
        if show_errors is None:
            if 'show_errors' in treq:
                show_errors = treq.show_errors
            else:
                show_errors = self.validation_errors > 0
        # doctor up the bunch
        #        data = data_to_dictionary_types(data, self.manager.project.mtsdict)
        subject = self.subject_with_overlaid_data(data)
        primary_data = subject.primary_chars.get(treq.default_source, {})
        translator = render.SurveyCommandTranslator(primary_data, show_errors)
        transforms = render.BasicTransformList(translator.translate)
        pipeline = self.manager.project.getpipeline(self.current_page.tree,
            subject, treq, render_transforms=transforms)
        return pipeline.run()
    
    def _advance(self, subject=None, treq=None):
        # need to doctor up the bunch as above
        if treq is None:
            treq = Bunch(default_source=self.manager.source)
        if subject is None:
            subject = self.subject
        context = self.manager.project.get_eval_factory(treq)(
            subject.selection_chars)
        try:
            ignore_loose_validation = self.validation_errors > 0
            if self.manager.can_pass_page(self.current_page, context,
                    ignore_loose_validation):
                self.current_page = self.manager.next_page(self.current_page)
                self.validation_errors = 0
                return True
        except GotoDestination, gd:
            self.current_page = gd.page
            self.validation_errors = 0
            return True
        except ValidationError:
            self.validation_errors += 1
            raise
        return False
    
    def handle_submit(self, data={}, treq=None):
        """Respond to a request to advance the subject to the next page of the
        survey. The result is a boolean indicating whether the subject was
        advanced to another Page, where self.current_page is consequently set
        to the new Page.
        All arguments are optional:
        - data: a flat, unsourced dictionary-like object, containing any
            values to be overlaid on self.subject before validating the
            current page.  The content will be applied to
            self.manager.source (or treq.default_source, if present) after
            being coerced to dictionary types.
        - treq: a tailoring2 tailoring request object passed along to the
            project's evaluation context factory.
        If there are no validation errors (which are raised to the caller),
        one of three actions may occur.
        - proceed to the next page: self.current_page will be reassigned to
            the next page in the survey. If a goto condition is satisified,
            self.current_page is set to the destination assigned by that goto.
            True is returned.
        - the end of the survey is reached: if there are no more pages to
            display, EndOfSurvey is raised.
        - a blank page is encountered: if for some reason a page produces no
            content to be rendered for the subject, and does not contain any
            errors in processing, the survey will attempt to advance through
            the survey, as above, until it finds a page with content or
            errors.  If a suitible page is found, True is returned, and
            self.current_page is at the appropriate page.  If no suitable page
            is found, EndOfSurvey is raised.
        """
#        data = data_to_dictionary_types(data, self.manager.project.mtsdict)
        subject = self.subject_with_overlaid_data(data)
        passed = self._advance(subject, treq)
        if passed:
            # check for empty pages post-render
            next_page, errors = self.render(data)
            try:
                while not tree_has_content(next_page) and not errors:
                    if self._advance(subject, treq):
                        next_page, errors = self.render(data)
                    else:
                        break
            except EndOfSurvey:
                raise
            except Exception, e:
                print 'broken', e
                pass
        return passed
    
    def advance_to_a_current_page(self, greedy=False):
        while self.current_page is not None:
            try:
                if not greedy:
                    chars_in_page = self.current_page.characteristics
                    keys = set(self.subject.keys())
                    if not ( chars_in_page & keys ):
                        return
                if not self._advance():
                    return
            except (InsufficientDataError, ValidationError):
                break
    
    def advance_to_page_id(self, id):
        self.current_page = self.manager.page_with_id(id)
    
    def get_manager(self):
        return self.manager
    
    def get_subject(self):
        return self.subject
    
    def set_subject(self,subject):
        self.subject = subject    
    
    def get_current_page(self):
        return self.current_page
    
    def set_current_page(self, page):
        self.current_page = page
        self.validation_errors = 0
    

def dump_pages(pages):
    for i, p in enumerate(pages):
        ET.ElementTree(p.tree).write('Page%d.survey' % ( i + 1 ))
