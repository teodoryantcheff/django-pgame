try:
    import simplejson as json
except ImportError:
    import json

from urllib import unquote_plus

import dogecoinrpc

import account.views
import account.forms

import pgameapp.forms

from pgameapp import utils

__author__ = 'Jailbreaker'


class LoginView(account.views.LoginView):
    form_class = account.forms.LoginEmailForm


class SignupView(account.views.SignupView):
    form_class = pgameapp.forms.SignupForm

    def get(self, *args, **kwargs):

        for ref_param in ['ref_code', 'ref_src', 'ref_cmp']:
            if not self.request.session.get(ref_param):
                self.request.session[ref_param] = self.request.GET.get(ref_param, None)

        # TODO
        print 'Referral parameters ref_code:"{}" ref_src:"{}" ref_cmp:"{}"'.format(
            self.request.session.get('ref_code'),
            self.request.session.get('ref_src'),
            self.request.session.get('ref_cmp')
        )

        return super(SignupView, self).get(*args, **kwargs)

    def generate_username(self, form):
        # do something to generate a unique username (required by the
        # Django User model, unfortunately)
        username = "<magic>"
        return username

    def after_signup(self, form):
        # Read and parse the referal cookie off the request if there is one
        # tracking_cookie = self.request.COOKIES.get('ref', '{}')
        # tracking_cookie = unquote_plus(tracking_cookie)
        # ref_info = json.loads(tracking_cookie)

        # and set that on the user profile
        user = self.created_user
        up = user.profile
        # up.set_referral_info(ref_code=ref_info.get('ref_code', None))
        up.set_referral_info(
            ref_code=self.request.session.get('ref_code', None),
            ref_source=self.request.session.get('ref_src', None),
            ref_campaign=self.request.session.get('ref_cmp', None),
        )

        conn = dogecoinrpc.connect_to_local('d:\\doge\\rpc.conf')
        crypto_address = conn.getnewaddress(account=user.email)
        up.crypto_address = crypto_address

        up.signup_ip = utils.get_client_ip(self.request) or ''
        up.nickname = user.email.split('@')[0][:20]

        up.save()

        super(SignupView, self).after_signup(form)
