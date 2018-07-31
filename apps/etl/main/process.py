# -*- coding: utf-8 -*-
# from apps.etl.main.database import Oradb
import os,time
import shutil
from subprocess import *
from python_etl.settings import MEDIA_ROOT

class TaskProcesser:

    def __init__(self,task_args):
        self.db_config = {'7','mk/mk@wtbzdb1',
                          '8','sjgl/sjgl@sjgl_new'}
        self.source_file_path = task_args["source_file_path"] # type: str
        self.task_id = self.source_file_path.split("\\")[-1].split(".")[0]
        self.task_path = MEDIA_ROOT +'\\process\\' +self.source_file_path.split("\\")[-1].split(".")[0]
        if self.task_id not in os.listdir(MEDIA_ROOT +'\\process\\'):
            os.mkdir(self.task_path)
            shutil.copy(self.source_file_path,self.task_path)
            os.chdir(self.task_path)
        self.source_file_path = self.task_path + '\\' +self.source_file_path.split("\\")[-1]
        self.target_table = task_args['target_table']
        self.truncate = 'truncate' if task_args['truncate'] == '1' else ''
        self.target_container = task_args['target_container']
        self.log_file =''


    def _createCSV(self):
        # 读取CSV文件表头，生成导入对应列信息
        with open(self.source_file_path, 'r', encoding='gbk') as f:
            title_line = f.readline()
        title = [l.replace('\n', '') for l in title_line.split(',')]
        _column_str = ''
        for t in title:
            _column_str += t + '  ' + 'char(100)' + ',\n'
        column_str = _column_str[:-2]
        # 数据库方法
        # db = Oradb(task_args['target_container'])
        # columns_lst= db.columns(task_args['target_table'])
        # _column_str=''
        # for columns in columns_lst:
        #     _column_str += columns['COLUMN_NAME'] + '    ' +'CHAR'+'('+'100'+')'+',\n'
        # column_str = _column_str[:-2]
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
                '''.format(self.source_file_path, self.target_table, self.truncate, column_str)
        ctl_name = self.task_id + '.ctl'
        with open(ctl_name, 'w+', encoding='utf-8') as ctl_f:
            ctl_f.write(ctl_content)

        return

    def _createBat(self):
        ctl_name=self.task_id +'.ctl'
        # bat
        userid = self.db_config[self.target_container]
        bat_content = '''
        sqlldr userid={0} control={1} log={2} bad={3}
        '''.format(userid,ctl_name,self.task_id.split('.')[0] + '.log',self.task_id.split('.')[0] + '.bad')
        bat_name = self.task_id + '.bat'
        with open(bat_name, 'w+', encoding='utf-8') as bat_f:
            bat_f.write(bat_content)
        return


    def doBat(self):
        self._createCSV()
        self._createBat()
        bat_name = self.task_id + '.bat'
        p = Popen(bat_name,stdout=PIPE,stderr=PIPE)
        while p.poll() is None :
            count_now=p.stdout.readline().decode('cp936').split(' ')[-1]
            return count_now
        self.log_file = self.source_file_path.split('.')[0] +'.log'
        return 'done'



    def testBat(self,task_args):
        task_args['task_status'] = 'recived'
        return task_args

    def reviewCSV(self,filePath):
        csv_file = open(filePath,'r',encoding='gbk')
        tr = []
        null_count = 0

        for line in csv_file:
            if len(line.replace('\n','').replace('"',''))>0:
                    tr.append(line.replace('\n','').replace('"','').split(','))
            else:
                null_count += 1
        tr_review = tr[:100]
        json_dic = {'tr':tr_review,'null_count':null_count,'total_count':len(tr)}
        #self.create_csv()
        csv_file.close()

        return json_dic

    def close(self,file):
        file.colse()
        return

if __name__ == '__main__':
    task_args = {'target_container': '7',
                  'task_status': 'recived',
                  'target_table': 'python_etl_test',
                  'source_table': '', 'target_sql': '',
                  'source_file_path': 'E:\\project\\python_etl\\media\\upload\\etl\\FDFDFD_20180727110339.csv',
                  'user_name': '杨哲',
                  'truncate': '1',
                  'source_sql': '',
                  'source_container': '1'}

    test = TaskProcesser(task_args)
    print(test.source_file_path)
