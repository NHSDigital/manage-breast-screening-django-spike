from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Clinic, ClinicSlot, Provider, Setting

admin.site.register(Clinic, SimpleHistoryAdmin)
admin.site.register(ClinicSlot, SimpleHistoryAdmin)
admin.site.register(Provider, SimpleHistoryAdmin)
admin.site.register(Setting, SimpleHistoryAdmin)
