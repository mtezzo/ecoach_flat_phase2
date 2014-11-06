import re
import string
import datetime
import itertools
import sys
from random import choice, randrange

from django.contrib.auth.models import User

class Code(object):
    """Represents a single access code object. Can be queried for validity and
    existence in the authentication system. Class methods exist for new code
    generation."""
    
    def __init__(self, accesscode):
        self.accesscode = accesscode
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.accesscode)
    
    def is_valid(self):
        """Identifies whether the current Code is valid per the rules defined
        by the class."""
        return True
    
    def get_user(self):
        """Returns the Django Authentication package User model associated
        with this code. If no such user exists, raises User.DoesNotExist."""
        return User.objects.get(username=self.accesscode)
    
    def create_user(self):
        """Returns a new Django Authentication package User model for this
        new access code, set without a password or last_login time. Returns
        None if the code already exists."""
        try:
            u = User.objects.create(username=self.accesscode)
        except:
            exception = sys.exc_info()
            print "Unexpected error:", sys.exc_info()
            return None
        else:
            u.set_unusable_password()
            u.last_login = datetime.datetime(1904, 1, 1)
            u.save()
            return u
    
    def get_or_create_user(self):
        """Returns a Django Authenication package User model for this code,
        along with a boolean indicating whether the user was created or
        not."""
        try:
            return self.get_user(), False
        except User.DoesNotExist:
            return self.create_user(), True
    
    @classmethod
    def generate_new_code(cls):
        """Subclasses should implement this class method to customize how
        access codes strings are built. This method should not attempt to
        check whether a code it generated was already used."""
        chars = string.ascii_letters + string.digits
        return ''.join(choice(chars) for _ in range(15))
    
    @classmethod
    def code_generator(cls):
        while True:
            yield cls.generate_new_code()
    
    @classmethod
    def codes_in_database(cls, codes):
        current_users = User.objects.filter(username__in=list(codes))
        return [user.username for user in current_users.all()]
    
    @classmethod
    def new_code(cls):
        """Returns a single properly-classed Code instance that does not have
        an associated User in the database."""
        return cls.new_codes(1).pop()
    
    @classmethod
    def new_codes(cls, size):
        """Returns a set of properly-classed Code instances of size `size`.
        Codes returned are guaranteed not to have Users in the database at the
        time of generation."""
        codegen = cls.code_generator()
        codes = set()
        while len(codes) < size:
            codes.update(itertools.islice(codegen, size - len(codes)))
            codes -= set(cls.codes_in_database(codes))
        return set(cls(code) for code in codes)
    

_accesscode_re = re.compile(r'^[A-Za-z]{2}[0-9]{4}$')
class BasicAccessCode(Code):
    """A code class that generates codes in the format "LLDDDD", where L is
    an uppercase ASCII letter from the set containing A-T, and D is a
    base-10 digit."""
    
    valid_letters = string.ascii_uppercase[:20]
    GENERATABLE_CODE_MAX_COUNT = 20 ** 2 * 10000
    
    def is_valid(self):
        return bool(_accesscode_re.match(self.accesscode))
    
    @classmethod
    def generate_new_code(cls):
        letter_gen = lambda: choice(cls.valid_letters)
        return '%s%s%04d' % (letter_gen(), letter_gen(), randrange(0, 10000))
    

class BasicTestCode(BasicAccessCode):
    """A BasicAccessCode whose letters will only be in the set of letters
    containing W-Z rather than A-T. This distinguishes them from regular
    BasicAccesCodes easily."""
    
    valid_letters = string.ascii_uppercase[22:]


# ---------- old functions ----------

def code_generator(valid_letters):
    letter_gen = lambda: choice(valid_letters)
    while True:
        yield '%s%s%04d' % (letter_gen(), letter_gen(), randrange(0, 10000))    

def accesscode_generator():
    return code_generator(string.ascii_uppercase[:20])

def testcode_generator():
    # leave a hole in the generators to ensure a fairly clean differentiation
    return code_generator(string.ascii_uppercase[22:])

def codes_in_db(codes):
    current_users = User.objects.filter(username__in=list(codes))
    if current_users.count() > 0:
        return [user.username for user in current_users.all()]
    return []

def new_unused_code(codegen=None):
    return new_unused_codes(1, codegen).pop()

def new_unused_codes(size, codegen=None):
    if codegen is None:
        codegen = accesscode_generator()
    codes = set()
    while len(codes) < size:
        codes.update(itertools.islice(codegen, size - len(codes)))
        codes -= set(codes_in_db(codes))
    return codes

def create_user_for_accesscode(code):
    try:
        u = User.objects.create(username=code)
    except:
        return None
    else:
        u.set_unusable_password()
        u.last_login = datetime.datetime(1904, 1, 1)
        u.save()
        return u

def is_valid_accesscode(code):
    return bool(_accesscode_re.match(code))
