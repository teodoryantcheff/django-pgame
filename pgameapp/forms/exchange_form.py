
from django import forms

from pgameapp.services import exchange__w2i

from . import ContextForm


__author__ = 'Jailbreaker'


class ExchangeForm(ContextForm):
    gc_to_exchange = forms.DecimalField(
        min_value=1,
        required=True,
        widget=forms.TextInput(attrs={'size': 5})
    )

    def clean(self):
        cleaned_data = super(ExchangeForm, self).clean()

        gc_to_exchange = cleaned_data.get('gc_to_exchange')
        exchange__w2i(self.request.user, gc_to_exchange)
