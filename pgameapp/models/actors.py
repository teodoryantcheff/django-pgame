from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from . import AUTH_USER_MODEL

__author__ = 'Jailbreaker'


class UserActorOwnership(models.Model):
    """
    Links users to owned actors
    """

    """
    FK to user
    """
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        null=False,
        blank=False
    )

    actor = models.ForeignKey(
        'Actor',
    )

    num_actors = models.PositiveIntegerField(
        verbose_name='number of actors',
        default=0
    )

    class Meta:
        unique_together = (('user', 'actor'),)

    def __unicode__(self):  # __str__ on python 3
        return u'UA <{}> {}x"{}"'.format(self.user, self.num_actors, self.actor)


class Actor(models.Model):
    """
    dogs / cats / flowers ... cash generators
    """
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    output = models.FloatField(default=0)

    image_path = models.CharField(
        verbose_name='actor image file location',
        max_length=50,
        blank=True,
        null=True
    )

    """
    Is the shit sellable
    """
    is_active = models.BooleanField(
        # verbose_name='Make sellable',
        default=True
    )

    """
    users having this actor
    """
    users = models.ManyToManyField(
        to=AUTH_USER_MODEL,
        through=UserActorOwnership,
    )

    def image_tag(self):
        if self.image_path:
            # FIXME !!! Fucking images and shit !!!
            # print u'<img src="%s" />' % (settings.STATIC_URL + self.image_path)
            return u'<img src="%s" />' % (settings.STATIC_URL + self.image_path)
        else:
            return ''
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        ordering = ['price']

    def __unicode__(self):  # __str__ on python 3
        return self.name


def on_user_creation(sender, instance, created, **kwargs):
    # TODO Actor bonuses go in here... maybe
    if created:
        print 'Adding actors to user', instance
        all_actors = Actor.objects.all()
        UserActorOwnership.objects.bulk_create(
            [UserActorOwnership(user=instance, actor=actor, num_actors=0) for actor in all_actors]
        )


post_save.connect(on_user_creation, sender=AUTH_USER_MODEL)