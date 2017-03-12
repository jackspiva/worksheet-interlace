from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from ws_interlace import views
from rest_framework.routers import DefaultRouter
from ws_interlace.views import WorksheetViewSet
from rest_framework import renderers

router = DefaultRouter()
router.register(r'worksheets', views.WorksheetViewSet)

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
