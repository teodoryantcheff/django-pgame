from django.db import models
import solo

from . import DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS

__author__ = 'Jailbreaker'


class ManualGameStats(solo.models.SingletonModel):
    """
    If any of these are not empty this is shown to the user instead of the official stats
    """
    users_total = models.PositiveIntegerField(blank=True)
    users_new_last_24 = models.PositiveIntegerField(blank=True)
    cash_total_paid = models.DecimalField(blank=True, max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_DECIMAL_PLACES)
    cash_reserve = models.DecimalField(blank=True, max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_DECIMAL_PLACES)
    project_duration_days = models.PositiveIntegerField(blank=True)
