from django.conf.urls.defaults import *

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^resetpassword/', 'password_reset',
        {'post_reset_redirect': '/accounts/resetmessagesent/',
         'template_name': 'accounts/password_reset_form.html',
         'email_template_name': 'accounts/password_reset_email.txt'},
        name='passwordreset'),
    url(r'^resetmessagesent/', 'password_reset_done',
        {'template_name': 'accounts/password_reset_done.html'}),
    url(r'^resetconfirm/(?P<uidb36>\w*)\|(?P<token>[\-a-zA-Z0-9]*)',
        'password_reset_confirm',
        {'post_reset_redirect': '/accounts/resetcomplete/',
         'template_name': 'accounts/password_reset_confirm.html'}),
    url(r'^resetcomplete/', 'password_reset_complete',
        {'template_name': 'accounts/password_reset_complete.html'}),
)
