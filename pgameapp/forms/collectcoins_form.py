from pgameapp.services import collect_coins

from . import ContextForm

__author__ = 'Jailbreaker'


class CollectCoinsForm(ContextForm):
    def clean(self):
        collect_coins(self.request.user)