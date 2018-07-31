from django.shortcuts import render
from apps.etl.form import taskForm
from python_etl.settings import MEDIA_ROOT
import time
from apps.etl.main.process import TaskProcesser
# from apps.etl.main.database import Oradb
from django.http import HttpResponse
from subprocess import *

# Create your views here.

COUNT_NOW ={}
def etlForm(request):
    task_args = {'user_name': '',
                'source_container': '',
                'source_sql':'',
                'souce_file_path': '',
                'target_container': '',
                'target_sql': '',
                'truncate': '',
                'task_status':''}

    if request.POST:
        t_p = TaskProcesser()
        task_args['user_name'] = request.POST['user_name']
        task_args['source_container'] = request.POST['source_container']
        task_args['target_container'] = request.POST['target_container']

        # 数据源信息 保存文件
        souce_file = request.FILES['source_file']
        souce_file_path = MEDIA_ROOT + r'\upload\etl' + '\\' + task_args['user_name'] + '_' +time.strftime('%Y%m%d%H%M%S',time.localtime()) +'.csv'

        with open(souce_file_path,'wb+') as f:
            for chunk in souce_file.chunks():
                f.write(chunk)
        task_args['source_file_path'] = souce_file_path
        global COUNT_NOW
        COUNT_NOW[souce_file_path]=''

        task_args['source_table'] = request.POST.get('source_table','')

        # 目标库信息
        task_args['target_table'] = request.POST['target_table']
        task_args['truncate'] = request.POST['truncate']

        task_args['task_status'] = 'sended'

        t_p = TaskProcesser(task_args)
        count_now =  t_p.doBat()
        while count_now !='done':
            return HttpResponse(count_now)
        log=[]
        with open(t_p.log_file,'r') as logs:
            for line in logs.readlines():
                log.append(line+"\n")
        return HttpResponse(log)
        # return render(request, 'etl/form.html', {'error': res})
    return render(request,'etl/form.html')

# 异步检查目标表是否存在
# def checkTable(request):
#     db = Oradb(request.POST['target_container'])
#     res = db.checkTable(request.POST['target_table'])[0][0]
#     return HttpResponse(res)

def showProgress(request):
    global COUNT_NOW
    return HttpResponse(COUNT_NOW)

def reviewCSV(request):
    if request.POST:
        error = ''
        form = taskForm(request.POST,request.FILES)
        if request.POST['user_name'] =='':
            error='填写用户名'
        user_name = request.POST['user_name']
        if not request.POST['source_container']:
            error='请选择数据源'
        source_container = request.POST['source_container']
        if str(form['source_file'].data) != 'None':
            if len(form['source_file'].data) > 0:
                souce_file = request.FILES['source_file']
                # 拼接文件保存路径
                souce_file_path = MEDIA_ROOT + r'\upload\etl' + '\\' + user_name + '_' + time.strftime(
                    '%Y%m%d%H%M%S', time.localtime()) + '.csv'
                # 保存文件
                with open(souce_file_path, 'wb+') as f:
                    for chunk in souce_file.chunks():
                        f.write(chunk)
                tp = TaskProcesser()
                json_str = tp.reviewCSV(souce_file_path)
                return render(request, 'etl/reviewCSV.html',{'json_str':json_str,
                                                                 'error':error,
                                                                'mode':1})
            else:
                error = '文件为空'
        else:
            error = '未选择上传文件'
        return render(request, 'etl/reviewCSV.html', {'error': error})