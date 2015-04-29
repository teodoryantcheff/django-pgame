from django.db import models

from pgameapp.models import AbstractBaseUserHistory
from . import AUTH_USER_MODEL, DECIMAL_DECIMAL_PLACES, DECIMAL_MAX_DIGITS


__author__ = 'Jailbreaker'

# Create your models here.


class ApprovedWithdrawalRequestManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedWithdrawalRequestManager, self).get_queryset().filter(status=WithdrawalRequest.APPROVED)


class DeniedWithdrawalRequestManager(models.Manager):
    def get_queryset(self):
        return super(DeniedWithdrawalRequestManager, self).get_queryset().filter(status=WithdrawalRequest.DENIED)


class PendingWithdrawalRequestManager(models.Manager):
    def get_queryset(self):
        return super(PendingWithdrawalRequestManager, self).get_queryset().filter(status=WithdrawalRequest.PENDING)


class WithdrawalRequest(AbstractBaseUserHistory):
    APPROVED = 'A'
    PENDING = 'P'
    DENIED = 'D'
    PAID = '$'
    STATUS_CHOICES = (
        (APPROVED, 'approved'),
        (PENDING, 'pending'),
        (DENIED, 'denied'),
        (PAID, 'paid'),
    )

    """
    """
    amount = models.DecimalField(
        default=0,
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_DECIMAL_PLACES
    )

    """
    """
    to_address = models.CharField(
        max_length=48
    )

    """
    FK to User (admin) who gave statement on the request
    """
    decided_by = models.ForeignKey(
        to=AUTH_USER_MODEL,
        blank=True,
        null=True
    )

    """
    """
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=PENDING,
        blank=False
    )

    # Meta
    class Meta:
        ordering = ('-timestamp',)
        get_latest_by = 'timestamp'

    # Managers
    objects = models.Manager()
    approved = ApprovedWithdrawalRequestManager()
    denied = DeniedWithdrawalRequestManager()
    pending = PendingWithdrawalRequestManager()

    def __unicode__(self):  # __str__ on python 3
        return u'{status} {amount:.3f} to <{user}>'.format(
            status=self.status,
            amount=self.amount,
            user=self.user
        )



