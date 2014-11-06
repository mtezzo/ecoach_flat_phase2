import logging

from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from djangotailoring.accounts.models import GroupAccessCode, BasicGroupAccessCode

logger = logging.getLogger(__name__)

class EmailModelBackend(ModelBackend):
    
    def authenticate(self, email=None, password=None):
        try:
            logger.info('Attempting to authenticate user "%s".', email,
                extra={'class': self.__class__.__name__})
            user = User.objects.get(email=email)
            if user.check_password(password):
                logger.info('User authenticated.')
                return user
            logger.info('User password mismatch.')
        except User.DoesNotExist:
            logger.info('User not found.')
            return None
    

class AccessCodeBackend(ModelBackend):
    groupcode_class = GroupAccessCode
    
    def authenticate(self, accesscode=None):
        try:
            logger.info('Attempting to authenticate access code "%s".',
                accesscode, extra={'class': self.__class__.__name__})
            logger.debug('Checking to see if it is a group access code.')
            groupcode = self.groupcode_class.objects.get(groupcode=accesscode)
            logger.debug('"%s" is a group access code.', accesscode)
            new_code = groupcode.generate_new_subcode()
            if new_code is None:
                logger.warning('Group access code "%s" is exhausted.', accesscode)
                return None
            logger.debug('New code generated is "%s".', new_code.accesscode)
            user = new_code.create_user()
            logger.debug('User created and authenticated.')
            return user
        except self.groupcode_class.DoesNotExist:
            logger.debug('"%s" is not a group access code.', accesscode)
            pass # if this is not a group access code, move along.
        try:
            logger.info('Checking for individual access code.')
            user = User.objects.get(username=accesscode)
            if not (user.email and user.has_usable_password()):
                logger.info('User authenticated.')
                return user
            logger.info('User with access code has completed account setup.')
        except User.DoesNotExist:
            logger.info('No user with access code found.')
            return None
        return None
    

class BasicAccessCodeBackend(AccessCodeBackend):
    groupcode_class = BasicGroupAccessCode
