from django.http import HttpResponse
from django.shortcuts import render

from apps.etl.form import TaskForm
from apps.etl.main.database import Oradb
from apps.etl.main.process import TaskProcesser
from apps.etl.models import DataContainer


# Create your views here.

def etlForm(request):
    if request.method=='POST':
        form = TaskForm(request.POST,request.FILES)
        if form.is_valid():
            task_info = form.save()
            tp = TaskProcesser(task_info)
            log = tp.doBat(task_info)
            log_list = []
            with open(log,'r') as log_file:
                for line in log_file.readlines():
                    if line.replace("\n","") == "":
                        continue
                    ln = line.replace("  ","").split(",")
                    log_list.append(ln)
            return render(request,'etl/reviewCSV.html',{'title':'结果报告','csv_list':log_list[-15:-10],'cnt':'..'})
        return render(request, 'etl/errors.html', {'errors': form.errors.as_data()})
    else:
        return render(request,'etl/form.html',{'source_cons':DataContainer.objects.filter(type__in=['database','upload']),
                                               'target_cons': DataContainer.objects.filter(type__in=['database', 'download']),
                                               'uploads':[ i.id for i in DataContainer.objects.filter(type='upload')],
                                                'downloads':[i.id for i in DataContainer.objects.filter(type='download')]})

# 异步检查目标表是否存在
def checkTable(request):
    db = Oradb(request.POST['db_info'])
    res = int(db.checkTable(request.POST['table_name'])[0][0])
    return HttpResponse(res)
# 创建目标表
def createTable(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        table_name = request.POST.get('table_name')
        # 读取CSV文件表头，生成导入对应列信息
        title_line = csv_file.readline().decode('gbk')
        title = [l.replace('\n', '') for l in title_line.split(',')]
        column_str ='    varchar2(100),\n'.join(title).strip() + '    varchar2(100)'
        create_str = """
CREATE TABLE {0}
({1})
        """.format(table_name.upper(),column_str)
        return HttpResponse(create_str)
# 执行创建语句
def doCreate(request):
    if request.method == "POST":
        sql = request.POST.get('sql')
        db = Oradb(request.POST.get('db_info'))
        result = db.excute(sql)
        return HttpResponse(result)
# 查询进度
def showProgress(request):
    db = Oradb(request.POST['db_info'])
    cnt_target = int(db.countTable(request.POST['table_name'])[0][0])
    return HttpResponse(cnt_target)
# 预览文件
def reviewCSV(request):
    if request.method == "POST":
        csv_file = request.FILES['file']
        csv_list = []
        i = 1
        for line in csv_file.readlines():
            ln = line.decode('gbk').split(",")
            ln.insert(0,i)
            csv_list.append(ln)
            i += 1
        return  render(request,'etl/reviewCSV.html',{'title':'预览100行','csv_list':csv_list[:100],'cnt':len(csv_list)})