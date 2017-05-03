# stdlib imports
import os
from io import BytesIO

# core django imports
from django.template.defaultfilters import slugify
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files import File
from django.conf import settings

# 3rd party app imports
from urllib.request import urlopen

# imports from my apps
from ws_interlace.number_recognition.internal_api import parseNumberImage, test, trainDigits


class Classroom(models.Model):
    name = models.CharField(null=True, max_length=100)
    teacher = models.CharField(null=True, max_length=100)


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    student_id = models.IntegerField(null=True)
    name = models.CharField(null=True, max_length=100)
    classroom = models.ManyToManyField(
        Classroom, related_name='students', blank=True)


def get_remote_image(ans):
    if ans.image_url and not ans.image_file:
        response = urlopen(ans.image_url)
        io = BytesIO(response.read())
        ans.image_file.save(os.path.basename(ans.image_url), File(io))
        ans.save()


class Worksheet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    classroom = models.ForeignKey(
        Classroom, related_name="worksheets", null=True)


class Section(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True, default='')
    section_type = models.CharField(max_length=100, blank=True, default='')
    worksheet = models.ForeignKey(
        Worksheet, related_name='sections', null=True, blank=True)

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    student_name = models.CharField(max_length=100, blank=True, default='')
    text = models.CharField(max_length=100, blank=True, default='')
    num = models.IntegerField(default=0)
    section = models.ForeignKey(
        Section, related_name='answers', null=True, blank=True)
    image_file = models.ImageField(upload_to='images', default='')
    image_url = models.URLField(default='')
    student = models.ForeignKey(
        Student, related_name="answers", null=True, blank=True, default=None)


def get_image_path(instance, filename):
    return '/'.join(['answer_images', instance.answer.id, filename])


# @receiver(post_save, sender=Answer)
# def begin_image_processing(sender, **kwargs):
#     if kwargs.get('created', False):
#         ans = kwargs.get('instance')
#         get_remote_image(ans)
#         print("FILE:", ans.image_file)
#         result = parseNumberImage(ans.image_file)
#         ans.num = result
#         ans.save()
