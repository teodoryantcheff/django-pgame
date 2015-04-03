#  forms.py
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from account.models import EmailAddress
from django import forms
from django.conf import settings

from pgameapp.models import Actor, UserActorOwnership
from pgameapp.services import collect_coins, sell_coins_to_gc, buy_actor, exchange__gc_w_to_i


class ContextForm(forms.Form):
    """
    Generic form that has Context on it -- passed in kwargs['request'].
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ContextForm, self).__init__(*args, **kwargs)


class CollectCoinsForm(ContextForm):
    def clean(self):
        collect_coins(self.request.user)


class StoreForm(ContextForm):
    def clean(self):
        cleaned_data = super(StoreForm, self).clean()
        # TODO error handling
        actor_id = int(self.data['actor'])
        print actor_id
        # print cleaned_data['actor']
        actor = Actor.objects.get(pk=actor_id)
        buy_actor(self.request.user, actor)


class SellCoinsForm(ContextForm):
    coins_to_sell = forms.DecimalField(required=True, min_value=0)

    def clean(self):
        cleaned_data = super(SellCoinsForm, self).clean()
        coins_to_sell = cleaned_data.get('coins_to_sell')
        sell_coins_to_gc(self.request.user, coins_to_sell)


class ExchangeForm(ContextForm):
    gc_to_exchange = forms.IntegerField(
        min_value=1,
        required=True,
    )

    def clean(self):
        cleaned_data = super(ExchangeForm, self).clean()

        gc_to_exchange = cleaned_data.get('gc_to_exchange')
        exchange__gc_w_to_i(self.request.user, gc_to_exchange)


class SignupForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label=_("Email"),
        widget=forms.TextInput())
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    code = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data
