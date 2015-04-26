import socket
from bitcoinrpc.authproxy import AuthServiceProxy
from pgameapp import wallet
from pgameapp.models import User

try:
    import simplejson as json
except ImportError:
    import json

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

        # TODO logging
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
        user.__class__ = User
        # up.set_referral_info(ref_code=ref_info.get('ref_code', None))
        user.set_referral_info(
            ref_code=self.request.session.get('ref_code') or '',
            ref_source=self.request.session.get('ref_src') or '',
            ref_campaign=self.request.session.get('ref_cmp') or '',
        )

        try:
            w = AuthServiceProxy(wallet.CRYPTO_WALLET_CONNSTRING)
            crypto_address = w.getnewaddress(user.email)
            user.set_crypto_address(crypto_address)
        except socket.error:
            # TODO Proper error handling here
            user.profile.crypto_address = '<pending>'

        user.profile.signup_ip = utils.get_client_ip(self.request) or ''
        user.profile.nickname = user.email.split('@')[0][:20]

        user.profile.save()

        super(SignupView, self).after_signup(form)
