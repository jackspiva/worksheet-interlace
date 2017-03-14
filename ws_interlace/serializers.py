from rest_framework import serializers
from ws_interlace.models import Worksheet, Answer


class WorksheetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Worksheet
        fields = ('title', 'description')


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Answer
        fields = ('title', 'description', 'student', 'text', 'worksheet', 'num',)
