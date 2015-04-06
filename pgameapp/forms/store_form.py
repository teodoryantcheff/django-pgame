

from pgameapp.models import Actor
from pgameapp.services import buy_actor

from . import ContextForm

__author__ = 'Jailbreaker'


class StoreForm(ContextForm):
    def clean(self):
        cleaned_data = super(StoreForm, self).clean()
        # TODO error handling
        actor_id = int(self.data['actor'])
        print actor_id
        # print cleaned_data['actor']
        actor = Actor.objects.get(pk=actor_id)
        buy_actor(self.request.user, actor)