from django.contrib.auth import get_user_model
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

    actor = models.ForeignKey('Actor',)

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


def create_blank_uas_for_user(sender, instance, created, **kwargs):
    """
    Creates blank UserActorOwnership entries for a newly added User
    Intended to be called in a signal receiver on post_save for User (EmailUser in this case)
    """

    if created:
        # print 'Adding actors to user', instance
        UserActorOwnership.objects.bulk_create(
            [UserActorOwnership(user=instance, actor=actor, num_actors=0) for actor in Actor.objects.all()]
        )


def add_uas_to_users_on_new_actor(sender, instance, created, **kwargs):
    """
    Creates blank UserActorOwnership entries to all users for a newly added Actor
    Intended to be called in a signal receiver on post_save for Actor
    """

    if created:
        # Add actor to all users
        UserActorOwnership.objects.bulk_create(
            [UserActorOwnership(user=user, actor=instance) for user in sender.objects.all()]
        )


post_save.connect(
    create_blank_uas_for_user,
    sender=AUTH_USER_MODEL,
    dispatch_uid='post_save__User__create_blank_uas_for_user'
)

post_save.connect(
    add_uas_to_users_on_new_actor,
    sender=Actor,
    dispatch_uid='add_uas_to_users_on_new_actor'
)


#
# def delete_uas_from_users(sender, instance, using, **kwargs):
#     """
#     Triggered by a signal on Actor deletion. Deletes all UserActorOwnership referring the to be deleted Actor
#     """
#     UserActorOwnership.objects.filter(actor=instance).delete()
#
# pre_delete.connect(
#     delete_uas_from_users,
#     sender=Actor,
#     dispatch_uid='delete_uas_from_users'
# )