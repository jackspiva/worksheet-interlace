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
import urllib
# imports from my apps
from ws_interlace.number_recognition.internal_api import parseNumberImage, test, trainDigits
from ws_interlace.text_recognition.internal_api import processWordList, refinedProcessWordList


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
    roster = models.TextField(blank=True, null=True, default='')


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
    student_id = models.IntegerField(null=True)
    student_name = models.CharField(max_length=100, blank=True, default='')
    text = models.CharField(max_length=100, blank=True, default='-')
    num = models.IntegerField(default=0)
    section = models.ForeignKey(
        Section, related_name='answers', null=True, blank=True)
    image_file = models.ImageField(upload_to='images', default='')
    image_url = models.URLField(default='')


def get_image_path(instance, filename):
    return '/'.join(['answer_images', instance.answer.id, filename])


def get_remote_image(ans):
    print("SAVE THIS:" + str(ans.image_url))
    if ans.image_url and not ans.image_file:
        result = urllib.request.urlretrieve(ans.image_url)
        ans.image_file.save(
            os.path.basename(ans.image_url),
            File(open(result[0]))
        )
        ans.save()


@receiver(post_save, sender=Answer)
def begin_image_processing(sender, **kwargs):
    print("listener")
    if kwargs.get('created', False):
        ans = kwargs.get('instance')
        sec = ans.section
        ws = sec.worksheet
        classList = ws.roster
        wordList = classList.split(", ")
        collabList = processWordList(ans.image_url)
        refinedCollabList = refinedProcessWordList(ans.image_url, wordList)
        collabString = ', '.join(map(str, collabList))
        refinedCollabString = ', '.join(map(str, refinedCollabList))
        print(collabList)
        if sec.section_type == "Names":
            ans.student_name = refinedCollabString
        else:
            nameSec = Section.objects.filter(
                worksheet=ws).filter(name="Names")
            nameAns = Answer.objects.filter(
                section=nameSec).filter(student_id=ans.student_id)
            nameAns = list(nameAns)
            desiredName = nameAns[0]
            ans.student_name = desiredName.student_name
            if sec.section_type == "Collaborators":
                ans.text = refinedCollabString
            elif sec.section_type == "Numbers":
                ans.num = int(collabString)
                # get_remote_image(ans)
                # result = parseNumberImage(ans.image_file)
                # ans.num = result

        ans.save()
