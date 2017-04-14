from django.shortcuts import render
from django.views.generic.detail import DetailView

from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.http import *
import json

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
    sections = Section.objects.all()
    answers = Answer.objects.all()
    sections_dict = {}
    for ws in worksheets:
        sections_dict[ws.name] = list(Section.objects.filter(worksheet=ws))

    answers_dict = {}
    for section in sections:
        answers_dict[section.name] = list(Answer.objects.filter(section=section))


    return render(request, 'index.html', {'worksheets': worksheets, 'secs': sections_dict})


def make_table_data(request):
    data_string = request.GET.get('json_data')
    ws_names = list(Worksheet.objects.values_list('name', flat=True).order_by('id'))
    data_dict = json.loads(data_string)
    ws_name = data_dict['ws_name']
    ws = Worksheet.objects.get(name=ws_name)
    section_list = list(Section.objects.filter(worksheet=ws))
    print(ws.name)
    f = open('/Users/johnspiva/Google Drive/Programming/worksheet-project/ws_interlace/static/ajax/data.txt', 'w')
    table_data = {}
    table_data["data"] = []
    i = 0
    for s in section_list:
        print("i")
        if i < len(ws_names):
            table_data["data"].append([ws_names[i], s.name])
        else:
            table_data["data"].append(["-", s.name])

        i = i + 1
    while i < len(ws_names):
        table_data["data"].append([ws_names[i], "-"])




    print(table_data["data"])
    json.dump(table_data, f)
    return HttpResponse()

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
