from django.contrib import admin
from app import models

# Register your models here.
class UserJwcxAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_last_login',)
    #显示外键表中的字段
    def get_last_login(self, obj):
        return obj.user.last_login


class CloudAdmin(admin.ModelAdmin):
    list_display = ('name', 'web_site', 'link_man', 'phone', 'qq')

class CustomersAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_man', 'phone', 'email', 'address')

class HostsAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_from', 'ip', 'private_ip', 'bandwidth', 'os_system')
    filter_horizontal = ('host_group',)

class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('com_name', 'name',  'domain', 'status', 'exp_date')
    filter_horizontal = ('on_server',)
    list_filter = ('exp_date', 'status')


admin.site.register(models.UserJwcx, UserJwcxAdmin)
admin.site.register(models.ServerGroup)
admin.site.register(models.Cloud, CloudAdmin)
admin.site.register(models.Customers, CustomersAdmin)
admin.site.register(models.Hosts, HostsAdmin)
admin.site.register(models.Projects, ProjectsAdmin)

