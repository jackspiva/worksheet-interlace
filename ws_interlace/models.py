from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models


class Worksheet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True, default='')
    description = models.TextField(blank=True, null=True, default='')

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    section_id = models.CharField(max_length=100, blank=True, default='')
    section_name = models.CharField(max_length=100, blank=True, default='')
    student_id = models.CharField(max_length=100, blank=True, default='')
    student_name = models.CharField(max_length=100, blank=True, default='')
    text = models.CharField(max_length=100, blank=True, default='')
    num = models.IntegerField(default=0)
    worksheet = models.ForeignKey(Worksheet, related_name='answers', null=True)


def get_image_path(instance, filename):
    return '/'.join(['answer_images', instance.answer.main_view, filename])
