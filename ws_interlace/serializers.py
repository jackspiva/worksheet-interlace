from rest_framework import serializers
from ws_interlace.models import Worksheet, Answer


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Answer
        fields = ('title', 'description', 'student',
                  'text', 'worksheet', 'num',)


class WorksheetSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Worksheet
        fields = ('title', 'description', 'answers',)

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        worksheet = Worksheet.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(worksheet=worksheet, **answer_data)
        return worksheet
