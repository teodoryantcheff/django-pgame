

from django import forms
from pgameapp.services import sell_coins_to_gc

from . import ContextForm


__author__ = 'Jailbreaker'


class SellCoinsForm(ContextForm):
    coins_to_sell = forms.DecimalField(
        required=True,
        min_value=0,
        # widget=forms.TextInput(attrs={'size': 5})
        # widget=forms.NumberInput(attrs={'max-width': '5em'})
    )

    def clean(self):
        cleaned_data = super(SellCoinsForm, self).clean()
        coins_to_sell = cleaned_data.get('coins_to_sell')
        sell_coins_to_gc(self.request.user, coins_to_sell)

