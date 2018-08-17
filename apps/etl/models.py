import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
def source_file_path(instance,filename):
    today = datetime.datetime.today().strftime(format='%Y%m%d%H%M%S')
    source_container_name = instance.source_container.name if instance.source_container.name !='上传CSV文件' else 'CSV'
    task_name = source_container_name + '-'+ instance.target_container.name +'-'+ instance.target_table.upper()
    # MEDIA_ROOT/process/user_name/createtime/filename
    return "process/{0}/{1}/{2}".format(instance.user_name.upper(),today,filename)

class DataContainer(models.Model):
    name = models.CharField(max_length=30,default='temp_'+datetime.datetime.today().strftime(format='%Y%m%d%H%M%S'))
    type = models.CharField(max_length=20,default='未分类')
    user_id = models.CharField(max_length=30,null=True,blank=True,default=None)
    pass_word = models.CharField(max_length=30,null=True,blank=True,default=None)
    ip = models.GenericIPAddressField(protocol='IPv4',null=True,blank=True,default=None)
    port = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(65535)],null=True,blank=True,default=0)
    service_name = models.CharField(max_length=30,null=True,blank=True,default=None)

    def __str__(self):
        return self.name

class Task(models.Model):
    user_name = models.CharField(max_length=30)
    source_container = models.ForeignKey('DataContainer',related_name='SourceContainer',on_delete=models.SET_NULL,null=True)
    source_file= models.FileField(upload_to=source_file_path,blank=True)
    source_table = models.CharField(max_length=30,null=True,blank=True)
    target_container = models.ForeignKey('DataContainer',related_name='TargetContainer',on_delete=models.SET_NULL,null=True)
    target_table = models.CharField(max_length=30,null=True,blank=True)
    truncate = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    cnt_source = models.CharField(max_length=100,default='0',null=True,blank=True)
    cnt_target = models.CharField(max_length=100,default='0',null=True,blank=True)
    status = models.CharField(max_length=10,default='等待',null=True,blank=True)
    complete_time = models.DateTimeField(auto_now=True)

