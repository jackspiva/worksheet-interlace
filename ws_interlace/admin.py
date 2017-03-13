from django.contrib import admin

# Register your models here.
from ws_interlace.models import Worksheet, Answer, Upload

admin.site.register(Worksheet)
admin.site.register(Answer)
admin.site.register(Upload)
