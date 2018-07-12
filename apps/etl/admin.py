from django.contrib import admin
from apps.etl.models import ETLUser, sourceContainer, targetContainer

# Register your models here.
class AdminETLUser(admin.ModelAdmin):
    list_display = ('user_name',
                  'source_container',
                  'source_sql',
                  'source_file',
                  'target_container',
                  'target_sql',
                  'truncate')

class AdminSourceContainer(admin.ModelAdmin):
    list_display = ('name','type')

class AdminTargetContainer(admin.ModelAdmin):
    list_display = ('name','type')

admin.site.register(ETLUser,AdminETLUser)
admin.site.register(sourceContainer,AdminSourceContainer)
admin.site.register(targetContainer,AdminTargetContainer)