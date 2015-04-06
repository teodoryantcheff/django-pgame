from django import forms
from django.core.exceptions import ValidationError
from pgameapp.models import GameConfiguration


from . import RequestContextForm


__author__ = 'Jailbreaker'


class SellCoinsForm(RequestContextForm):
    coins_to_sell = forms.DecimalField(
        required=True,
        min_value=0,
        # widget=forms.TextInput(attrs={'size': 5})
        # widget=forms.NumberInput(attrs={'max-width': '5em'})
    )

    def clean_coins_to_sell(self):
        # cleaned_data = super(SellCoinsForm, self).clean()
        coins_to_sell = self.cleaned_data.get('coins_to_sell')

        game_config = GameConfiguration.objects.get(pk=1)
        user = self.request.user

        if coins_to_sell > user.profile.balance_coins:
            raise ValidationError('Not enough coins in balance')

        if coins_to_sell < game_config.min_coins_to_sell:
            raise ValidationError('Need to sell at least {}'.format(game_config.min_coins_to_sell))

        return coins_to_sell
