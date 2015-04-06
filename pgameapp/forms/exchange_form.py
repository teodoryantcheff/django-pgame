
from django import forms
from django.core.exceptions import ValidationError
from pgameapp.models import GameConfiguration

from pgameapp.services import exchange__w2i

from . import RequestContextForm


__author__ = 'Jailbreaker'


class ExchangeForm(RequestContextForm):
    gc_to_exchange = forms.DecimalField(
        min_value=1,
        required=True,
        widget=forms.NumberInput(attrs={'size': 5}),
        max_digits=10,
        decimal_places=0
    )

    def clean_gc_to_exchange(self):
        user = self.request.user
        gc_to_exchange = self.cleaned_data.get('gc_to_exchange')

        if gc_to_exchange > user.profile.balance_w:
            raise ValidationError('Not enough withdrdawal balance')

        return gc_to_exchange
