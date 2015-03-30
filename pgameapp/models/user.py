from django.db import models

from custom_user.models import EmailUser

__author__ = 'Jailbreaker'


class AdminsManager(models.Manager):
    def get_queryset(self):
        return super(AdminsManager, self).get_queryset().filter(is_staff=True)


class User(EmailUser):
    class Meta:
        proxy = True

    objects = models.Manager()
    admins = AdminsManager()

    def test(self):
        print '{} test on TUser'.format(self)
