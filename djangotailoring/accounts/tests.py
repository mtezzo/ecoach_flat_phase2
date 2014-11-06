"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import random

from django.test import TestCase
from django.contrib.auth.models import User

from djangotailoring.accounts.accesscodes import *
from djangotailoring.accounts.backends import *
from djangotailoring.accounts.models import *
from djangotailoring.accounts.forms import *

class SetupRoot(TestCase):
    def setUp(self):
        # set the randomizer to a constant seed on each run. 
        random.seed(0)
        self.code = self.code_class.new_code()
    
    def tearDown(self):
        pass
    

class CodeRoot(object):
    code_class = Code
    groupcode_class = GroupAccessCode
    first_code = '0UAqFzWsDK4FrUM'

class BasicAccessCodeRoot(object):
    code_class = BasicAccessCode
    groupcode_class = BasicGroupAccessCode
    first_code = 'QP4205'

class BasicTestCodeRoot(object):
    code_class = BasicTestCode
    first_code = 'ZZ4205'


class BaseCodeTests(object):
    def test_generic_code_generator(self):
        self.assertEqual(self.first_code, self.code.accesscode)
        self.assert_(self.code.is_valid())
        self.assertEqual(User.objects.filter(username=self.code.accesscode).count(), 0)
    
    def test_code_user_creation(self):
        u = self.code.create_user()
        self.assert_(u is not None)
        self.assert_(u in User.objects.all())
        self.assertEqual(u.username, self.code.accesscode)
    
    def test_code_user_fetching(self):
        self.assertRaises(User.DoesNotExist, self.code.get_user)
        u = self.code.create_user()
        u2 = self.code.get_user()
        self.assertEqual(u, u2)
    
    def test_get_or_create_user(self):
        user, created = self.code.get_or_create_user()
        self.assert_(created)
        self.assertEqual(user.username, self.code.accesscode)
        user2, created2 = self.code.get_or_create_user()
        self.assertFalse(created2)
        self.assertEqual(user, user2)
    
    def test_different_generations(self):
        code2 = self.code_class.new_code()
        self.assertNotEqual(self.code, code2)
    

class TestBaseCodeClass(CodeRoot, SetupRoot, BaseCodeTests):
    pass

class TestBasicAccessCodeClass(BasicAccessCodeRoot, SetupRoot, BaseCodeTests):
    pass

class TestBasicTestCodeClass(BasicTestCodeRoot, SetupRoot, BaseCodeTests):
    pass


class GroupSetupRoot(TestCase):
    
    def setUp(self):
        random.seed(0)
        self.groupcode_name = 'x'
        self.groupcode = self.groupcode_class.objects.create(
            groupcode=self.groupcode_name, usage_limit=3)
    

class GroupAccessCodeTests(object):
    
    def test_group_subcode_creation(self):
        subcode = self.groupcode.generate_new_subcode()
        self.assert_(subcode is not None)
        self.assertEqual(subcode.accesscode, self.first_code)
        self.assertEqual(GeneratedAccessCode.objects.all().count(), 1)
        self.assertEqual(GeneratedAccessCode.objects.filter(
            accesscode=subcode.accesscode).count(), 1)
        self.assertEqual(User.objects.all().count(), 0)
    
    def test_group_subcode_limits(self):
        subcode1 = self.groupcode.generate_new_subcode()
        self.assert_(subcode1 is not None)
        subcode2 = self.groupcode.generate_new_subcode()
        self.assert_(subcode2 is not None)
        subcode3 = self.groupcode.generate_new_subcode()
        self.assert_(subcode3 is not None)
        subcode4 = self.groupcode.generate_new_subcode()
        self.assert_(subcode4 is None)
        self.assertEqual(GeneratedAccessCode.objects.all().count(), 3)
        self.assertEqual(User.objects.all().count(), 0)
    

class TestGroupAccessCodes(CodeRoot, GroupSetupRoot, GroupAccessCodeTests):
    pass

class TestBasicGroupAccessCodes(BasicAccessCodeRoot, GroupSetupRoot, GroupAccessCodeTests):
    pass

class AccessCodeBackendTests(object):
    def test_valid_code(self):
        u1 = self.code.create_user()
        backend = self.backend_class()
        u = backend.authenticate(accesscode=self.first_code)
        self.assert_(u is not None)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(u, u1)
    
    def test_invalid_code(self):
        backend = self.backend_class()
        u = backend.authenticate(accesscode=self.first_code)
        self.assert_(u is None)
    
    def test_exhausted_code(self):
        u = self.code.create_user()
        u.email = 'x@y.com'
        u.set_password('password')
        u.save()
        backend = self.backend_class()
        u = backend.authenticate(accesscode=self.first_code)
        self.assert_(u is None)
    

class TestAccessCodeBackend(CodeRoot, SetupRoot, AccessCodeBackendTests):
    backend_class = AccessCodeBackend

class TestBasicAccessCodeBackend(BasicAccessCodeRoot, SetupRoot, AccessCodeBackendTests):
    backend_class = BasicAccessCodeBackend

class GroupAccessCodeBackendTests(object):
    def test_group_valid_user(self):
        backend = self.backend_class()
        u = backend.authenticate(accesscode=self.groupcode_name)
        self.assert_(u is not None)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(GeneratedAccessCode.objects.all().count(), 1)
        gac = GeneratedAccessCode.objects.get()
        self.assertEqual(gac.accesscode, u.username)
    
    def test_group_invalid_user(self):
        backend = self.backend_class()
        u = backend.authenticate(accesscode='')
        self.assert_(u is None)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertEqual(GeneratedAccessCode.objects.all().count(), 0)
    
    def test_overused_group(self):
        backend = self.backend_class()
        u1 = backend.authenticate(accesscode=self.groupcode_name)
        self.assert_(u1 is not None)
        u2 = backend.authenticate(accesscode=self.groupcode_name)
        self.assert_(u2 is not None)
        u3 = backend.authenticate(accesscode=self.groupcode_name)
        self.assert_(u3 is not None)
        u4 = backend.authenticate(accesscode=self.groupcode_name)
        self.assert_(u4 is None)
    

class TestGroupAccessCodeBackend(CodeRoot, GroupSetupRoot, GroupAccessCodeBackendTests):
    backend_class = AccessCodeBackend

class TestBasicGroupAccessCodeBackend(BasicAccessCodeRoot, GroupSetupRoot, GroupAccessCodeBackendTests):
    backend_class = BasicAccessCodeBackend

class TestEmailModelBackend(TestCase):
    def setUp(self):
        self.emb = EmailModelBackend()
        self.user = User.objects.create_user(username='x', email='x@y.com',
            password='password')
    
    def test_valid_email(self):
        u = self.emb.authenticate(email='x@y.com', password='password')
        self.assert_(u is not None)
        self.assertEqual(u.username, 'x')
    
    def test_invalid_email(self):
        u = self.emb.authenticate(email='y@x.com', password='password')
        self.assert_(u is None)
    
    def test_invalid_password(self):
        u = self.emb.authenticate(email='x@y.com', password='wrong')
        self.assert_(u is None)
    
    def test_not_using_username(self):
        u = self.emb.authenticate(email='x', password='password')
        self.assert_(u is None)
    

