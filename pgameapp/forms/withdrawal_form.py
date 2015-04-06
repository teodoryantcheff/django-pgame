# coding=utf-8
import socket
from django import forms
from django.core.exceptions import ValidationError

from bitcoinrpc.authproxy import AuthServiceProxy

from pgameapp import wallet
from . import RequestContextForm
from pgameapp.models import GameConfiguration, WithdrawalRequest

__author__ = 'Jailbreaker'


class WithdrawalForm(RequestContextForm):
    gc_to_withdraw = forms.DecimalField(
        min_value=1,
        required=True,
        label=u'Моля ви са недейте, ама все пак колко :',
        # widget=forms.TextInput(attrs={'size': 5})
    )

    to_address = forms.CharField(
        max_length=48,
        required=True,
        label=u'Address to send $$$ to',
        widget=forms.TextInput(attrs={'size': 48})
    )

    def clean_gc_to_withdraw(self):
        user = self.request.user
        game_config = GameConfiguration.objects.get(pk=1)
        gc_to_withdraw = self.cleaned_data['gc_to_withdraw']
        # print 'gc', gc_to_withdraw

        depcount, depamount = user.get_deposits_info()
        if depamount < game_config.min_withdrawal_deposit_amount:
            raise ValidationError("Haven't deposited enough")

        if gc_to_withdraw < game_config.min_withdrawal_amount:
            raise ValidationError('Minimum withdrawal amount is {}'.format(game_config.min_withdrawal_amount))

        if user.profile.balance_w < gc_to_withdraw:
            raise ValidationError('Not enough funds')

        return gc_to_withdraw

    def clean_to_address(self):
        to_address = self.cleaned_data.get('to_address')
        # print 'addr', to_address
        try:
            w = AuthServiceProxy(wallet.CRYPTO_WALLET_CONNSTRING)
            addr_info = w.validateaddress(to_address)
            # print addr_info
            address_valid = addr_info.get('isvalid', False)
            if not address_valid:
                raise ValidationError('Address is not valid')
        except socket.error:
            # TODO Proper error handling here
            raise ValidationError('Connection to wallet lost, retry later, mofo.')
        return to_address

    def clean(self):
        cleaned_data = super(WithdrawalForm, self).clean()
        # print cleaned_data

        num_pending_requests = WithdrawalRequest.objects.\
            filter(user=self.request.user, status=WithdrawalRequest.PENDING).\
            count()

        if num_pending_requests > 0:
            raise ValidationError('You have pending requests !')

        # print 'Requested {gc_to_withdraw} to "{to_address}"'.format(**cleaned_data)

        return cleaned_data

