from functools import partial

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.utils.translation import ugettext_lazy as _

from djangotailoring.accounts.forms import AccessCodeForm, EmailAuthenticationForm

login = partial(auth_login, authentication_form=EmailAuthenticationForm)

def validate_access_code(request, redirect_url=None,
        template_name='accounts/accesscodelogin.html'):
    if redirect_url is None:
        redirect_url = '/'
    if request.method == 'POST':
        form = AccessCodeForm(request.POST)
        if form.is_valid():
            from django.contrib.auth import login
            login(request, form.get_user())
            return redirect(redirect_url)
    else:
        form = AccessCodeForm()
    return render_to_response(template_name, locals(),
        context_instance=RequestContext(request))

