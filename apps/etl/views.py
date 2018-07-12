from django.shortcuts import render
from apps.etl.form import taskForm
from python_etl.settings import MEDIA_ROOT
import time
# Create your views here.


def etlForm(request):
    if request.POST:
        user_name = request.POST['user_name']
        source_container = request.POST['source_container']
        test=[]
        if source_container =='1':

            souce_file = request.FILES['source_file']
            #拼接文件保存路径
            file_name = MEDIA_ROOT + r'\upload\etl' + '\\' + user_name + '_' +time.strftime('%Y%m%d%H%M%S',time.localtime()) +'.csv'
            test = [user_name, source_container,file_name]
            # 保存文件
            with open(file_name,'wb+') as f:
                for chunk in souce_file.chunks():
                    f.write(chunk)
            # 目标库信息
            target_container = request.POST['target_container']
            target_sql = request.POST['target_sql']
            truncate = True if 'truncate'in request.POST.key() else False
            test = [user_name, source_container, file_name,target_container,target_sql,truncate]


        return render(request,'etl/form.html',{'form':taskForm,
                                               'test':test})
    return render(request,'etl/form.html',{'form':taskForm})
