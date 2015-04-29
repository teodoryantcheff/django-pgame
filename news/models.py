from django.db import models

__author__ = 'Jailbreaker'


class PublishedNewstManager(models.Manager):
    def get_queryset(self):
        return super(PublishedNewstManager, self).get_queryset().filter(is_published=True)


class NewsEntry(models.Model):
    """
    A single news entry
    """

    """
    DateTine of the NewsEntry
    """
    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )

    """
    Short text summarizing the entry
    """
    summary = models.CharField(
        max_length=256,
        blank=False
    )

    """
    Content text
    """
    content = models.TextField()

    """
    Boolean flag if the entry is published
    """
    is_published = models.BooleanField(default=True)

    # Meta
    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'
        verbose_name_plural = "NewsEntries"

    # Managers
    objects = models.Manager()
    published = PublishedNewstManager()

    def __unicode__(self):  # __str__ on python 3
        return u'{timestamp} {summary}'.format(
            timestamp=self.timestamp,
            summary=self.summary
        )