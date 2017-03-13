from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from ws_interlace.models import Worksheet, Answer
from ws_interlace.serializers import WorksheetSerializer, AnswerSerializer
from django.shortcuts import render


class WorksheetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Worksheet.objects.all()
    serializer_class = WorksheetSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        ws_name = request.data['worksheet']
        request.data['worksheet'] = "/api/worksheets/%i/" % Worksheet.objects.filter(title=ws_name)[
            0].pk
        print(request.data['worksheet'])
        return super(self.__class__, self).create(request, *args, **kwargs)


def index(request):
    queryset = Worksheet.objects.all()
    return render(request, 'index.html', {'worksheets': queryset, })


def worksheet_detail(request, slug):
    worksheet = Worksheet.objects.get(slug=slug)
    answers = worksheet.answers.all()
    return render(request, 'worksheets/worksheet_detail.html', {
        'worksheet': worksheet,
        'answers': answers,
    })
