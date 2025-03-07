from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin
from import_export.admin import ImportExportActionModelAdmin

from externalizer.forms import EnvServerAdminForm, EnvServicePropertyAdminForm, EnvironmentAdminForm, PropertyAdminForm, EnvironmentPropertyAdminForm, ServicePropertyAdminForm, UserDetailsAdminForm
from externalizer.models import EnvServer, Environment, Property, EnvironmentProperty, ServiceProperty, EnvServiceProperty, UserDetails

class EnvironmentAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["envName"]
    search_fields = ['envName',]
    form = EnvironmentAdminForm
    

class PropertyAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["propertyName", "environmentSpecific", "serviceSpecific"]
    search_fields = ['propertyName',]
    form = PropertyAdminForm
    

class EnvironmentPropertyAdmin(admin.ModelAdmin):
    list_display = ["environment", "prop", "propertyValue"]
    form = EnvironmentPropertyAdminForm
    

class ServicePropertyAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["service", "prop", "propertyValue"]
    list_filter = ["service__serviceName", "prop__propertyName"]
    form = ServicePropertyAdminForm
    

class EnvServicePropertyAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["serviceProperty", "environment", "propertyValue", "propertyTag", "propertyEnabled"]
    list_filter = ["environment__envName", "serviceProperty__service__serviceName", "serviceProperty__prop__propertyName"]
    form = EnvServicePropertyAdminForm
    

class EnvServerAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["environment", "server"]
    form = EnvServerAdminForm


class UserDetailsAdmin(DjangoQLSearchMixin, ImportExportActionModelAdmin):
    list_display = ["user", "repositoryURL"]
    form = UserDetailsAdminForm


admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(EnvironmentProperty, EnvironmentPropertyAdmin)
admin.site.register(ServiceProperty, ServicePropertyAdmin)
admin.site.register(EnvServiceProperty, EnvServicePropertyAdmin)
admin.site.register(EnvServer, EnvServerAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
