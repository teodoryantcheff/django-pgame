from django.core.exceptions import ValidationError
from django.utils import timezone
from pgameapp.models import GameConfiguration
from pgameapp.services import collect_coins

from . import RequestContextForm

__author__ = 'Jailbreaker'


class CollectCoinsForm(RequestContextForm):

    def __init__(self, *args, **kwargs):
        self.until = kwargs.pop('until', None)
        print 'form until', self.until
        super(CollectCoinsForm, self).__init__(*args, **kwargs)

    def clean(self):
        game_config = GameConfiguration.objects.get(pk=1)
        user = self.request.user

        last_coll = user.profile.last_coin_collection_time
        until = self.until  # timezone.now()

        seconds = int((until - last_coll).total_seconds())

        if seconds < game_config.coin_collect_time*60:
            raise ValidationError('Too soon')
