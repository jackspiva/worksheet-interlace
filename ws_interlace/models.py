from __future__ import unicode_literals

from django.db import models


class Worksheet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    student = models.CharField(max_length=100, blank=True, default='')
    text = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(unique=True)
    worksheet = models.ForeignKey(
        to=Worksheet, related_name="answers", blank=True, null=True)


def get_image_path(instance, filename):
    return '/'.join(['answer_images', instance.answer.main_view, filename])


class Upload(models.Model):
    answer = models.OneToOneField(
        Answer,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=get_image_path)
