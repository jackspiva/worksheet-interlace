import os
import urllib

from django.core.files import File

from rest_framework import serializers

from ws_interlace.models import Section, Answer, Worksheet, Student, Classroom


def get_remote_image(ans):
    print("SAVE THIS:" + str(ans.image_url))
    if ans.image_url and not ans.image_file:
        result = urllib.urlretrieve(ans.image_url)
        ans.image_file.save(
            os.path.basename(ans.image_url),
            File(open(result[0]))
        )
        ans.save()


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = ('name', 'student_id', 'classroom', 'answers', 'id',)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Answer
        fields = ('student', 'text', 'section',
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
            answers_data = section_data.pop('answers')
            section = Section.objects.create(
                worksheet=worksheet, **section_data)
            for answer_data in answers_data:
                Answer.objects.create(section=section, **answer_data)
        return worksheet

    class Meta:
        model = Worksheet
        fields = ('name', 'description', 'id', 'sections', 'classroom',)


class ClassroomSerializer(serializers.HyperlinkedModelSerializer):
    # students = StudentSerializer(many=True)
    worksheets = WorksheetSerializer(many=True)
    print("here1")

    def create(self, validated_data):
        # students_data = validated_data.pop('students')
        worksheets_data = validated_data.pop('worksheets')
        classroom = Classroom.objects.create(**validated_data, id=1)
        classroom.save()
        # s = {}
        # i = 0
        print("here1")
        # for student_data in students_data:
        # Student.objects.create(classroom=classroom, **student_data)
        # s[i].classrooms.add(classroom)
        # i = i + 1

        print("here2")
        # Student.objects.bulk_create(students_data)
        for worksheet_data in worksheets_data:
            Worksheet.objects.create(
                classroom=classroom, **worksheet_data)

        print("here3")

        return classroom

    class Meta:
        model = Classroom
        fields = ('name', 'students', 'worksheets', 'id',)
