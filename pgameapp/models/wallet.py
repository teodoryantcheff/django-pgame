from django.db import models


__author__ = 'Jailbreaker'


class BlockProcessingHistory(models.Model):
    """
    History of block processing
    """

    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )

    """
    blockhash
    """
    blockhash = models.CharField(
        max_length=128,
        null=False,
        blank=False
    )

    """
    blockheight for the block with hash blockhash
    """
    blockheight = models.BigIntegerField(
        default=0
    )

    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'
        verbose_name_plural = 'BlockProcessingHistory'

    def __unicode__(self):  # __str__ on python 3
        return u'BlockProcessingHistory'