from apps.etl.main.process import TaskProcesser
from subprocess import *
import time

task_args = {'target_container': '7',
             'task_status': 'recived',
             'target_table': 'python_etl_test',
             'source_table': '', 'target_sql': '',
             'source_file_path': 'E:\\project\\python_etl\\media\\upload\\etl\\FDFDFD_20180727110339.csv',
             'user_name': '杨哲',
             'truncate': '1',
             'source_sql': '',
             'source_container': '1'}

test = TaskProcesser()
now_path, bat_name = test.getFilesReady(task_args)
p = Popen(bat_name, stdout=PIPE, stderr=PIPE)
while p.poll() is None:
    count_now = p.stdout.readline().decode('cp936').split(' ')[-1]
    print(count_now)