import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class EmailAuthenticationForm(forms.Form):
    """
    Copied and hacked from the built-in django.contrib.auth.forms
    AuthenticationForm class. Don't hate.
    """
    email = forms.EmailField(label=_("Email address"), max_length=255)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    
    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        self.check_for_test_cookie()
        return self.cleaned_data
    
    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))
    
    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None
    
    def get_user(self):
        return self.user_cache
    

class AccessCodeForm(forms.Form):
    """A form to validate and find the user associated with an access code."""
    accesscode = forms.CharField(max_length=20, label=_("Access Code"))
    error_messages = {
        'invalid': _("You have entered an invalid access code."),
    }
    
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AccessCodeForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        accesscode = self.cleaned_data.get('accesscode')
        
        if accesscode:
            self.user_cache = authenticate(accesscode=accesscode)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid'])
        
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(
                    _("Your Web browser doesn't appear to have cookies "
                      "enabled. Cookies are required for logging in."))
        
        return self.cleaned_data
    
    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None
    
    def get_user(self):
        return self.user_cache
    

class CompleteUserForm(forms.Form):
    """A form used to enter a valid email address and pair of passwords for
    completion of account setup."""
    email = forms.EmailField(label=_("E-mail address"), max_length=75)
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CompleteUserForm, self).__init__(*args, **kwargs)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is not None:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
            raise forms.ValidationError(_("The email address provided is already registered."))
        return email
    
    def save(self, commit=True):
        """
        Saves the new password.
        """
        self.user.email = self.cleaned_data['email']
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user
    
