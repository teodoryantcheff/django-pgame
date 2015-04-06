# coding=utf-8

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings
from account.models import EmailAddress


class RequestContextForm(forms.Form):
    """
    Generic form that has Context on it -- passed in kwargs['request'].
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RequestContextForm, self).__init__(*args, **kwargs)


from collectcoins_form import CollectCoinsForm
from exchange_form import ExchangeForm
from sellcoins_form import SellCoinsForm
from store_form import StoreForm
from withdrawal_form import WithdrawalForm


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

