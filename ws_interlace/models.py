from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models


class Worksheet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, null=True, default='')

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    student = models.CharField(max_length=100, blank=True, default='')
    text = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(unique=True)
    num = models.IntegerField(default=5)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Answer, self).save(*args, **kwargs)
    worksheet = models.ForeignKey(Worksheet, related_name='answers', null=True)


def get_image_path(instance, filename):
    return '/'.join(['answer_images', instance.answer.main_view, filename])


class Upload(models.Model):
    answer = models.OneToOneField(
        Answer,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    title = models.CharField(max_length=100, blank=True, default='')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)

        super(Upload, self).save(*args, **kwargs)
    image = models.ImageField(upload_to=get_image_path)
