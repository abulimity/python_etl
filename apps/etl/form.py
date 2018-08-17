from django.forms import ModelForm

from apps.etl.models import Task


class TaskForm(ModelForm):

    class Meta:
        model=Task
        fields='__all__'
        labels = {'user_name': '姓名',
                  'source_container':'数据来源',
                  'source_file':'选择CSV文件',
                  'source_table':'数据源表名',
                  'target_container':'目标数据库',
                  'target_table':'目标表名',
                  'truncate':'清空目标表',}
        # widgets = {'user_name': forms.TextInput(attrs={'class':'form-control'})}
