from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from slugify import slugify

from pgameapp.models import Actor, GameConfiguration

from . import RequestContextForm

__author__ = 'Jailbreaker'


# class StoreForm(RequestContextForm):
#     def clean(self):
#         cleaned_data = super(StoreForm, self).clean()
#         # TODO error handling
#         actor_id = int(self.data['actor'])
#         print actor_id
#         # print cleaned_data['actor']
#         actor = Actor.objects.get(pk=actor_id)
#         buy_actor(self.request.user, actor)


class StoreForm(RequestContextForm):
    actor = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    def clean_actor(self):
        actor_id = self.cleaned_data['actor']
        print 'clean_actor actor_id="{}"'.format(actor_id)

        try:
            actor = Actor.objects.get(pk=actor_id)
            return actor
        except Actor.DoesNotExist:
            raise ValidationError('Illegal actor')

    def clean(self):
        cleaned_data = super(StoreForm, self).clean()

        game_config = GameConfiguration.objects.get(pk=1)
        actor = cleaned_data['actor']
        user = self.request.user

        print 'Actor "{}", price {}'.format(slugify(actor.name), actor.price)

        if actor.price > user.profile.balance_i:
            raise ValidationError('Insufficient funds')

        now = timezone.now()
        seconds = (now - user.profile.last_coin_collection_time).total_seconds()

        # If user has actors and hasn't collected
        if seconds > game_config.coin_collect_time*60 and user.get_total_actors() > 0:
            raise ValidationError('Go collect your shit first')

        return cleaned_data