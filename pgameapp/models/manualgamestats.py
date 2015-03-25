from django.db import models
import solo

__author__ = 'Jailbreaker'


class ManualGameStats(solo.models.SingletonModel):
    """
    If any of these are not empty this is shown to the user instead of the official stats
    """
    users_total = models.PositiveIntegerField(blank=True)
    users_new_last_24 = models.PositiveIntegerField(blank=True)
    cash_total_paid = models.FloatField(blank=True)
    cash_reserve = models.FloatField(blank=True)
    project_duration_days = models.PositiveIntegerField(blank=True)
