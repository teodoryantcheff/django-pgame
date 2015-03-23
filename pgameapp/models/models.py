from django.db import models
from django.conf import settings

import solo.models

__author__ = 'Jailbreaker'

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

# Create your models here.


class ManualGameStats(solo.models.SingletonModel):
    """
    If any of these are not empty this is shown to the user instead of the official stats
    """
    users_total = models.PositiveIntegerField(blank=True, null=True)
    users_new_last_24 = models.PositiveIntegerField(blank=True, null=True)
    cash_total_paid = models.FloatField(blank=True, null=True)
    cash_reserve = models.FloatField(blank=True, null=True)
    project_duration_days = models.PositiveIntegerField(blank=True, null=True)

