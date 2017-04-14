from django.shortcuts import render
from django.views.generic.detail import DetailView

from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Worksheet, Section, Answer
from .serializers import SectionSerializer, AnswerSerializer, WorksheetSerializer


class WorksheetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Worksheet.objects.all()
    serializer_class = WorksheetSerializer


class SectionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


def index(request):
    worksheets = Worksheet.objects.all()
    sec = {}
    for ws in worksheets:
        sec[ws.name] = list(Section.objects.filter(worksheet=ws))

    print(sec[worksheets[0].name])
    return render(request, 'index.html', {'worksheets': worksheets, 'secs': sec})


def worksheet_detail(request, pk, sect_id):
    worksheets = Worksheet.objects.all()
    worksheet = Worksheet.objects.get(pk=pk)
    sec = {}
    for ws in worksheets:
        sec[ws.name] = list(Section.objects.filter(worksheet=ws))
        print(sec[ws.name])

    sections = Section.objects.filter(worksheet=worksheet)
    sections = list(sections)
    section = Section.objects.get(pk=sect_id)
    answers = list(Answer.objects.filter(section=section))

    return render(request, 'worksheets/worksheet_detail.html', {
        'worksheets': worksheets,
        'worksheet': worksheet,
        'section': section,
        'secs': sec,
        'answers': answers
    })
