from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

class UserPassesTestMixin(object):
    """A simple mix-in class that forces any access of the implementing view
    class to be accessible only to logged-in users.
    """
    redirect_field_name=REDIRECT_FIELD_NAME
    login_url=None
    
    def dispatch(self, request, *args, **kwargs):
        super_dispatch = super(UserPassesTestMixin, self).dispatch
        protected_dispatch = user_passes_test(
            self.user_passes_test,
            self.get_login_url(),
            self.get_redirect_field_name())(super_dispatch)
        return protected_dispatch(request, *args, **kwargs)
    
    def user_passes_test(self, user):
        return True
    
    def get_login_url(self):
        return self.login_url
    
    def get_redirect_field_name(self):
        return self.redirect_field_name
    

class LoginRequiredMixin(UserPassesTestMixin):
    """A simple mix-in class that forces any access of the implementing view
    class to be accessible only to logged-in users.
    """
    
    def user_passes_test(self, user):
        return user.is_authenticated()
    

