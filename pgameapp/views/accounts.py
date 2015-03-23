try:
    import simplejson as json
except ImportError:
    import json

import django.utils.http

import account.views
import account.forms

import pgameapp.forms
from pgameapp.services import create_userprofile

__author__ = 'Jailbreaker'


class LoginView(account.views.LoginView):
    form_class = account.forms.LoginEmailForm


class SignupView(account.views.SignupView):
    form_class = pgameapp.forms.SignupForm

    def generate_username(self, form):
        # do something to generate a unique username (required by the
        # Django User model, unfortunately)
        username = "<magic>"
        return username

    def after_signup(self, form):
        # Read and parse the referal cookie off the request if there is one
        tracking_cookie = self.request.COOKIES.get('ref', '{}')
        tracking_cookie = django.utils.http.unquote_plus(tracking_cookie)
        ref_info = json.loads(tracking_cookie)

        # Actually create the user profile
        create_userprofile(form.cleaned_data['email'], ref_info)

        super(SignupView, self).after_signup(form)
