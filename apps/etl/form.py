from django import forms
from apps.etl.models import sourceContainer, targetContainer
from django.forms import widgets


class taskForm(forms.Form):
    user_name = forms.CharField(label='姓名',max_length=30,widget=widgets.TextInput(attrs={'class':'form-control'}))
    source_container = forms.ModelChoiceField(label='数据来源',queryset=sourceContainer.objects.all(),empty_label='-------')
    source_file = forms.FileField(label='源文件')
    source_sql = forms.CharField(label='数据源SQL',widget=forms.Textarea)
    target_container = forms.ModelChoiceField(label='数据目标',queryset=targetContainer.objects.all(),empty_label='-------')
    target_sql = forms.CharField(label='目标数据库SQL',widget=forms.Textarea)
