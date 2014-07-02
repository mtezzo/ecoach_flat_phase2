import sys
import optparse
import os
import fnmatch
import itertools

import django.conf
from django.template import Context
from django.template.loaders import filesystem as fsloader
from django.core.management.base import CommandError
from django.core.management.commands.startapp import Command as SACommand
from django.template.defaultfilters import slugify

    
def namebase(pth):
    return os.path.splitext(os.path.basename(pth))[0]


class Command(SACommand):
    option_list = SACommand.option_list + (
        optparse.make_option('', '--mts-project',
            dest="mts_project",
            default=None,
            help="path to the MTS project",
        ),
    )
    
    def handle_label(self, app_name, directory=None, **options):
        if directory is None:
            directory = os.getcwd()

        try:
            mtsroot = options.get('mts_project') or django.conf.settings.TAILORING2_PROJECT_ROOT
        except AttributeError:
            mtsroot = None
        if mtsroot is None:
            raise CommandError("must specify --mts-project or define TAILORING2_PROJECT_ROOT in settings.py")
        if not os.path.exists(mtsroot):
            raise CommandError("MTS project '%s' not found!" % mtsroot)

        super(Command, self).handle_label(app_name, directory, **options)

        source_root_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(source_root_dir, 'surveyapp_templates')
        renderer = SurveyTemplateRenderer(mtsroot, app_name, templates_dir)
        
        def app_py_path(n):
            return os.path.join(directory, app_name, namebase(n) + '.py')
        def new_project_templates_folder():
            return os.path.join(directory, 'templates')
        def template_path(n):
            return os.path.join(new_project_templates_folder(), n)
            
        py_results = [(app_py_path(tname), renderer.render(tname))
                for tname in ['survey.pyt', 'views.pyt']]
        tfolder = new_project_templates_folder()
        if not os.path.exists(tfolder):
            os.makedirs(tfolder)
        template_results = [(template_path(tname), renderer.render(tname))
                for tname in ['survey.html']]
        all_results = list(itertools.chain(py_results, template_results))

        dest_dir = os.path.join(source_root_dir, app_name)
        for name, content in all_results:
            destpath = os.path.join(dest_dir, name)
            with open(destpath, 'wb') as f:
                f.write(content)
        

class SurveyTemplateRenderer:
    
    def __init__(self, mts_project_root, app_name, templates_dir):
        self.mts_project_root = mts_project_root
        self.app_name = app_name
        self.templates_dir = templates_dir
        self.loader = fsloader.Loader()
    
    def render(self, template_name):
        template, _ = self.loader.load_template(template_name,
            template_dirs=[self.templates_dir])
        context = Context(self.template_context())
        return template.render(context)
        
    def template_context(self):
        survey_pairs = [(slugify(namebase(pth)), self.relpath(pth)) for pth in self.survey_files()]
        if not survey_pairs:
            survey_pairs = [('ZZZ', 'Surveys/ZZZ.survey')]
        mts_project_surveys = [(name, pth, view_class_name(name))
                for name, pth in survey_pairs]
        controller_class_name = '%sSurveyController' % (self.app_name.capitalize())
        survey_view_pairs = [(name, view_class_name(name))
                for name, _ in survey_pairs]
        return dict(
            app_name=self.app_name,
            survey_tuples=repr(survey_pairs),
            mts_project_surveys=mts_project_surveys,
            controller_class_name=controller_class_name,
            survey_view_pairs=survey_view_pairs,
            survey_view_classes=[clsname for _, clsname in survey_view_pairs],
        )
    
    def survey_files(self):
        # walk the project for .survey files, return list of project-relative paths
        result = []
        for path, dirs, files in os.walk(self.mts_project_root):
            for f in files:
                if fnmatch.fnmatch(f, '*.survey'):
                    result.append(os.path.join(path, f))
        return result
        
    def relpath(self, p):
        return p.replace(self.mts_project_root + '/', '')


def view_class_name(surveyname):
    return '%sSurveyView' % surveyname.capitalize()


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = optparse.OptionParser()
    # add options here
    # ...
    opts, args = parser.parse_args(argv)
    if len(args) < 1:
        print "Usage: must supply path to MTS project"
        return 2
    if len(args) > 1:
        print "Usage: only one path"
        return 2
    
    mts_project_root = os.path.abspath(args[0])
    assert os.path.exists(mts_project_root)
    sys.path.append(os.path.join(os.path.dirname(mts_project_root), 'START_Django'))
    import django.conf
    django.conf.settings.configure(INSTALLED_APPS=('djangotailoring',),
        TAILORING2_PROJECT_ROOT=mts_project_root)
    
    templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'surveyapp_templates')
    assert os.path.exists(templates_dir)
    assert os.path.exists(os.path.join(templates_dir, 'survey.pyt'))
    renderer = SurveyTemplateRenderer(mts_project_root, 'dummy', templates_dir)
    for name in ['survey.pyt', 'views.pyt', 'survey.html']:
        content = renderer.render(name)
        print "# ------------------------------------------------------------"
        print name
        print content
        print


if __name__ == '__main__':
    sys.exit(main())
