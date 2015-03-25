from urllib import unquote_plus

try:
    import simplejson as json
except ImportError:
    import json

import account.views
import account.forms

import pgameapp.forms

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
        tracking_cookie = unquote_plus(tracking_cookie)
        ref_info = json.loads(tracking_cookie)

        # and sed to on the user proifle
        up = self.created_user.profile
        up.set_referral_info(ref_code=ref_info.get('ref_code', None))
        up.save()

        super(SignupView, self).after_signup(form)
