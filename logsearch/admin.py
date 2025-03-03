from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin
from import_export.admin import ImportExportActionModelAdmin

from logsearch.forms import ServerAdminForm, ServerUserAdminForm, ServiceAdminForm, LogFileAdminForm, ServiceLogFileAdminForm, ServerServiceAdminForm, ServerUserAdminForm, SysConfigAdminForm
from logsearch.models import Server, Service, LogFile, ServiceLogFile, ServerService, ServerUser, SysConfig

class ServerAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["serverName", "serverIP", "description", "defaultUser", "lockoutCredentials"]
    search_fields = ['serverName','serverIP',]
    form = ServerAdminForm
    

class ServiceAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["serviceName", "description"]
    search_fields = ['',]
    form = ServiceAdminForm
    

class LogFileAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["logFilename", "description", "defaultPath"]
    search_fields = ['logFilename',]
    form = LogFileAdminForm


class ServiceLogFileAdmin(admin.ModelAdmin):
    list_display = ["service", "logfile", "filePath"]
    form = ServiceLogFileAdminForm
    

class ServerServiceAdmin(admin.ModelAdmin):
    list_display = ["server", "service", "servicePath", "jarFile"]
    form = ServerServiceAdminForm
    

class ServerUserAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["server", "user", "loginUser", "lockoutCredentials"]
    form = ServerUserAdminForm


class SysConfigAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["configProperty", "configValue"]
    form = SysConfigAdminForm

admin.site.register(ServerUser, ServerUserAdmin)
admin.site.register(ServerService, ServerServiceAdmin)
admin.site.register(ServiceLogFile, ServiceLogFileAdmin)
admin.site.register(LogFile, LogFileAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(SysConfig, SysConfigAdmin)