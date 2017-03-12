from rest_framework import serializers
from ws_interlace.models import Worksheet


class WorksheetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Worksheet
        fields = ('title', 'description',)
