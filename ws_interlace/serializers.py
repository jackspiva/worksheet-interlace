import os
import urllib

from django.core.files import File

from rest_framework import serializers

from ws_interlace.models import Section, Answer, Worksheet


def get_remote_image(ans):
    print("SAVE THIS:" + str(ans.image_url))
    if ans.image_url and not ans.image_file:
        result = urllib.urlretrieve(ans.image_url)
        ans.image_file.save(
            os.path.basename(ans.image_url),
            File(open(result[0]))
        )
        ans.save()


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
        fields = ('name', 'worksheet', 'description', 'answers', 'id',)


class WorksheetSerializer(serializers.HyperlinkedModelSerializer):
    sections = SectionSerializer(many=True)

    def create(self, validated_data):
        sections_data = validated_data.pop('sections')
        worksheet = Worksheet.objects.create(**validated_data)
        for section_data in sections_data:
            Section.objects.create(worksheet=worksheet, **section_data)
        return section

    class Meta:
        model = Worksheet
        fields = ('name', 'description', 'id', 'sections')
