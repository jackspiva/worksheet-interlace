from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from ws_interlace import views
from rest_framework.routers import DefaultRouter
from ws_interlace.views import WorksheetViewSet, AnswerViewSet
from rest_framework import renderers
from django.views.generic import TemplateView
from django.conf import settings
# from rest_framework_swagger.views import get_swagger_view


# schema_view = get_swagger_view(title='Worksheet API')

router = DefaultRouter()
router.register(r'worksheets', views.WorksheetViewSet)
router.register(r'answers', views.AnswerViewSet)
urlpatterns = [
    url(r'^$', views.index, name='home'),
    # The new URL entries we're adding:
    url(r'^about/$',
        TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contact/$',
        TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^worksheets/(?P<slug>[-\w]+)/$', views.worksheet_detail,
        name='worksheet_detail'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api/docs/', schema_view),
]
