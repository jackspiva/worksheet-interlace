from __future__ import unicode_literals

from django.db import models


class Worksheet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, null=True, default='')

    class Meta:
        ordering = ('created',)
