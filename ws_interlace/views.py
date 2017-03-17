from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from ws_interlace.models import Worksheet, Answer
from ws_interlace.serializers import WorksheetSerializer, AnswerSerializer
from django.shortcuts import render
from django.views.generic.detail import DetailView


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


def index(request):
    queryset = Worksheet.objects.all()
    return render(request, 'index.html', {'worksheets': queryset, })


def worksheet_detail(request, pk):
    worksheet = Worksheet.objects.get(pk=pk)
    answers = worksheet.answers.all()
    ws_answers = worksheet.answers.all()
    return render(request, 'worksheets/worksheet_detail.html', {
        'worksheet': worksheet,
        'answers': answers,
        'ws_answers': ws_answers,
    })
