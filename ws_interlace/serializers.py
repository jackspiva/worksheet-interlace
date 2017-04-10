from rest_framework import serializers
from ws_interlace.models import Worksheet, Answer
from django.core.files import File
import os


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

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
