from django.contrib import admin

from apps.etl.models import Task, DataContainer


# Register your models here.
class AdminTask(admin.ModelAdmin):
    list_display = ('pk',
                  'user_name',
                  'source_container',
                  'source_table',
                  'source_file',
                  'target_container',
                  'target_table',
                  'truncate',
                  'create_time',
                  'status',
                  'cnt_target',
                  'cnt_source')

class AdminSourceContainer(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'type',
                    'user_id',
                    'pass_word',
                    'ip',
                    'port',
                    'service_name')

admin.site.register(Task,AdminTask)
admin.site.register(DataContainer,AdminSourceContainer)
