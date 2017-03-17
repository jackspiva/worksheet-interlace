from django.contrib import admin

# Register your models here.
from ws_interlace.models import Worksheet, Answer

admin.site.register(Worksheet)
admin.site.register(Answer)
