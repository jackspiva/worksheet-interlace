from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from ws_interlace import views
from rest_framework.routers import DefaultRouter
from ws_interlace.views import SectionViewSet, AnswerViewSet
from rest_framework import renderers
from django.views.generic import TemplateView, DetailView
from django.conf import settings


router = DefaultRouter()
router.register(r'sections', views.SectionViewSet)
router.register(r'answers', views.AnswerViewSet)
urlpatterns = [
    url(r'^$', views.index, name='home'),
    # The new URL entries we're adding:
    url(r'^about/$',
        TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contact/$',
        TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^sections/(?P<pk>[-\w]+)/$', views.section_detail,
        name='section_detail'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/docs/', TemplateView.as_view(template_name='docs/docs.html'), name='docs'),

]
