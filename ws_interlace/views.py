from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from ws_interlace.models import Worksheet
from ws_interlace.serializers import WorksheetSerializer
from django.shortcuts import render


class WorksheetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Worksheet.objects.all()
    serializer_class = WorksheetSerializer


def index(request):
    queryset = Worksheet.objects.all()
    return render(request, 'index.html', {'worksheets': queryset, })
