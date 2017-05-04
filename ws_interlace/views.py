from django.shortcuts import render
from django.views.generic.detail import DetailView

from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .models import Worksheet, Section, Answer
from .serializers import SectionSerializer, AnswerSerializer, WorksheetSerializer

from django.http import *
import json


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
    worksheet = Worksheet.objects.get(pk=1)
    for ws in worksheets:
        sec[ws.name] = list(Section.objects.filter(worksheet=ws))

    return render(request, 'index.html', {'worksheets': worksheets, 'secs': sec, 'ws': worksheet})


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


def get_sections(request):
    data_string = request.GET.get('json_data')
    data_dict = json.loads(data_string)
    ws_name = data_dict['ws_name']
    ws = Worksheet.objects.get(name=ws_name)
    section_list = list(Section.objects.filter(worksheet=ws))
    data = ""
    for s in section_list:
        list_item = "<tr><td id=\"" + s.name + "\"" + \
            " onClick=\"sec_click(\'" + str(s.id) + "\')\">" + \
            s.name + "</td></tr>"
        data += list_item
    return HttpResponse(data)


def get_answers(request):
    data_string = request.GET.get('json_data')
    data_dict = json.loads(data_string)
    sec_id = data_dict['sec_id']
    print("SECTION NAME: ", sec_id)
    sec = Section.objects.get(id=sec_id)
    sec_type = sec.section_type
    print("sectoin type is ", sec_type)
    answer_list = list(Answer.objects.filter(section=sec))
    ids = []
    names = []
    images = []
    nums = []
    names = []
    collaborators = []
    for a in answer_list:
        # list_item = "<button type=\"button\" class=\"list-group-item\"" + \
        #     " onClick=\"\">" + \
        #     str(a.num) + "</li>"
        # data += list_item
        ids.append(a.student_id)
        names.append(a.student_name)
        images.append(a.image_url)
        nums.append(a.num)
        collaborators.append(a.text)

    data = {}
    data['type'] = sec_type

    data['collaborators'] = collaborators

    data['ids'] = ids
    data['names'] = names
    data['images'] = images
    data['nums'] = nums
    data['section'] = sec.name
    data = json.dumps(data)

    return HttpResponse(data)
