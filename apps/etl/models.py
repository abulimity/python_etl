from django.db import models

# Create your models here.
class ETLUser(models.Model):
    user_name = models.CharField(max_length = 30)
    source_container = models.ForeignKey('sourceContainer',related_name='source_container',on_delete=models.SET_NULL,null=True)
    source_file= models.FileField(upload_to=r'upload\etl',blank=True)
    source_sql = models.TextField(null=True,blank=True)
    target_container = models.ForeignKey('targetContainer',related_name='target_container',on_delete=models.SET_NULL,null=True)
    target_sql = models.TextField(null=True)
    truncate = models.BooleanField(default=False)

class sourceContainer(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(default='未分类',max_length=20)

    def __str__(self):
        return self.name

class targetContainer(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(default='未分类',max_length=20)

    def __str__(self):
        return self.name

# class ETLUserForm(ModelForm):
#     class Meta:
#         model = ETLUser
#         fields = ['user_name',
#                   'source_container',
#                   'source_sql',
#                   'source_file',
#                   'target_container',
#                   'target_sql',
#                   'truncate']