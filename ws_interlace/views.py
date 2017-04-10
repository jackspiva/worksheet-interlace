from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from ws_interlace.models import Section, Answer
from ws_interlace.serializers import SectionSerializer, AnswerSerializer
from django.shortcuts import render
from django.views.generic.detail import DetailView


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
    queryset = Section.objects.all()
    return render(request, 'index.html', {'sections': queryset, })


def section_detail(request, pk):
    section = Section.objects.get(pk=pk)
    answers = section.answers.all()
    ws_answers = section.answers.all()
    return render(request, 'sections/section_detail.html', {
        'section': section,
        'answers': answers,
        'ws_answers': ws_answers,
    })
