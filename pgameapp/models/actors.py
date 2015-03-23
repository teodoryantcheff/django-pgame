from django.db import models
from django.conf import settings

__author__ = 'Jailbreaker'


AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class UserActorOwnership(models.Model):
    """
    Links users to owned actors
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
        return 'UA <{}> {}x"{}"'.format(self.user, self.num_actors, self.actor)


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

    def image_tag(self):
        if self.image_path:
            # FIXME !!! Fucking images and shit !!!
            # print u'<img src="%s" />' % (settings.STATIC_URL + self.image_path)
            return u'<img src="%s" />' % (settings.STATIC_URL + self.image_path)
        else:
            return ''
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    """
    Is the shit sellable
    """
    is_active = models.BooleanField(
        # verbose_name='Make sellable',
        default=True
    )

    """
    """
    users = models.ManyToManyField(
        to=AUTH_USER_MODEL,
        through=UserActorOwnership,
    )

    class Meta:
        ordering = ['price']

    def __unicode__(self):  # __str__ on python 3
        return self.name
