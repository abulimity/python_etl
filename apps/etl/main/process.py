# -*- coding: utf-8 -*-
import django
import os
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_etl.settings")
django.setup()
from apps.etl.main.database import Oradb
from subprocess import *
from python_etl.settings import MEDIA_ROOT


class TaskProcesser:

    def __init__(self,task_info):
        self.db_config = {'MK':'mk/mk@wtbzdb1',
                          '6':'mk/mk@wtbzdb1',
                          'SJGL':'sjgl/Ju8THs_sj@SJGL_NE',
                          '7':'sjgl/Ju8THs_sj@SJGL_NEW'}
        self.task = task_info
        self.source_file_path = MEDIA_ROOT  + '\\'+self.task.source_file.name.replace('/','\\')
        self.task_path = '\\'.join(self.source_file_path.split('\\')[:-1])
        source_container_name = re.sub(r'[^a-zA-Z0-9]',"",self.task.source_container.name)
        target_container_name = re.sub(r'[^a-zA-Z0-9]',"",self.task.target_container.name)
        self.task_name = source_container_name + '-' + target_container_name + '-' + self.task.target_table.upper()
        os.chdir(self.task_path)
        #记录数据文件行数

        with open(self.source_file_path,'r',encoding='gbk')as f:
            task_info.cnt_source = len(f.readlines())
            task_info.save()



    def _createCtl(self):

        # 数据库方法
        truncate = 'TRUNCATE' if self.task.truncate else ''
        db = Oradb(self.task.target_container.id)
        if truncate:
            db.truncateTable(self.task.target_table)
        columns_lst= db.columns(self.task.target_table)
        _column_str=''
        for columns in columns_lst:
            _column_str += columns['COLUMN_NAME'] + '    ' +'CHAR'+'('+'100'+')'+',\n'
        column_str = _column_str[:-2]
        ctl_content = '''
        LOAD DATA 
            INFILE '{0}'
            INTO TABLE {1}
            {2}
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
        TRAILING NULLCOLS
        (
        {3}
        )
                '''.format(self.source_file_path, self.task.target_table, truncate, column_str)
        ctl_name = self.task_name+ '.ctl'
        with open(ctl_name, 'w+', encoding='gbk') as ctl_f:
            ctl_f.write(ctl_content)
        return ctl_name

    def _createBat(self,ctl_name):
        # bat
        userid = self.db_config[self.task.target_container.name]
        bat_content = '''
        sqlldr userid={0} control={1} log={2} bad={3}  >> cur_log.log
        '''.format(userid,ctl_name,self.task_name + '.log',self.task_name + '.bad')
        bat_name = self.task_name + '.bat'
        with open(bat_name, 'w+', encoding='utf-8') as bat_f:
            bat_f.write(bat_content)
        return bat_name


    def doBat(self,task):
        bat_name = self._createBat(self._createCtl())
        p = Popen(bat_name,shell=True)
        task.status = '正在导入'
        task.save()
        # while p.poll() is None:
        #     pass
        p.wait()
        if p.returncode == 0:
            task.status = '已完成'
            task.save()
            print('Subprogram success')
        else:
            task.status = '报错'
            task.save()
            print('Subprogram failed:%s'%p.returncode)
        self.log_file = self.task_path + '\\'+ self.task_name +'.log'
        return self.log_file



    def testBat(self):
        return self.task_info.source_file


    def close(self,file):
        file.colse()
        return

if __name__ == '__main__':
    task_args = {'target_container': '7',
                  'task_status': 'recived',
                  'target_table': 'python_etl_test1',
                  'source_table': '',
                  'target_table': '',
                  'source_file_path': 'E:\\project\\python_etl\\media\\upload\\etl\\test_20180731184748.csv',
                  'user_name': '杨哲',
                  'truncate': '1',
                  'source_table': '',
                  'source_container': '1'}
    test_task = Task.objects.get(pk=85)
    tp = TaskProcesser(test_task)
    tp.doBat(test_task)


