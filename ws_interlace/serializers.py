import os


from django.core.files import File

from rest_framework import serializers

from ws_interlace.models import Section, Answer, Worksheet


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Answer
        fields = ('student_id', 'student_name', 'text', 'section',
                  'num', 'id', 'image_url', 'image_file')


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        section = Section.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(section=section, **answer_data)
        return section

    class Meta:
        model = Section
        fields = ('name', 'worksheet', 'description',
                  'answers', 'id', 'section_type')


class WorksheetSerializer(serializers.HyperlinkedModelSerializer):
    sections = SectionSerializer(many=True)

    def create(self, validated_data):
        sections_data = validated_data.pop('sections')
        worksheet = Worksheet.objects.create(**validated_data)
        for section_data in sections_data:
            answers_data = section_data.pop('answers')
            section = Section.objects.create(
                worksheet=worksheet, **section_data)
            for answer_data in answers_data:
                Answer.objects.create(section=section, **answer_data)
        return worksheet

    class Meta:
        model = Worksheet
        fields = ('name', 'description', 'id', 'sections', 'roster')
