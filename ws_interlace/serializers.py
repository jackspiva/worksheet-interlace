from rest_framework import serializers
from ws_interlace.models import Worksheet, Answer
from django.core.files import File
import os
import urllib


def get_remote_image(ans):
    if ans.image_url and not ans.image_file:
        result = urllib.urlretrieve(ans.image_url)
        ans.image_file.save(
            os.path.basename(ans.image_url),
            File(open(result[0]))
        )
        ans.save()


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        answer = Answer.objects.create(**validated_data)
        get_remote_image(answer)
        return answer

    class Meta:
        model = Answer
        fields = ('student_name', 'section_name', 'section_id',
                  'text', 'worksheet', 'num', 'id', 'image_url', 'image_file')


class WorksheetSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        worksheet = Worksheet.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(worksheet=worksheet, **answer_data)
        return worksheet

    class Meta:
        model = Worksheet
        fields = ('name', 'description', 'answers', 'id',)
