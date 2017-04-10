from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.files import File
import os
from urllib.request import urlretrieve

from ws_interlace.number_recognition.internal_api import parseNumberImage, parseCustomNumberImage, test, trainDigits

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
    student_name = models.CharField(max_length=100, blank=True, default='')
    text = models.CharField(max_length=100, blank=True, default='')
    # TODO: remove default to zero, also default empty strings on other
    # fields, that way we can only use data from field if it is valid when
    # creating bar chart and stuff
    num = models.IntegerField(default=0)
    worksheet = models.ForeignKey(Worksheet, related_name='answers', null=True)
    image_file = models.ImageField(upload_to='images', default='')
    image_url = models.URLField(default='')


def get_image_path(instance, filename):
    return '/'.join(['answer_images', instance.answer.id, filename])



@receiver(post_save, sender=Answer)
def begin_image_processing(sender, **kwargs):
    if kwargs.get('created', False):
        ans = kwargs.get('instance')
        #get_remote_image(ans)
        #result = parseCustomNumberImage(ans.image_file)
        result = parseNumberImage()
        print(result)
        print(ans.num)
        ans.num = result


def get_remote_image(ans):
    print("SAVE THIS:" + str(ans.image_url))
    if ans.image_url and not ans.image_file:
        result = urlretrieve(ans.image_url)
        ans.image_file.save(
            os.path.basename(ans.image_url),
            File(open(result[0]))
        )
        ans.save()