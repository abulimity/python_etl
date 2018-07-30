# -*- coding: utf-8 -*-
from apps.etl.main.database import Oradb
import os,time
import shutil
from subprocess import *



class TaskProcesser:
    def __init__(self):
        self.user_id = {
            '7':'mk/mk@wtbzdb1',
            '8':'sjgl/Ju8THs_sj@SJGL_NEW'
        }

    def getFilesReady(self,task_args):
        # taskArgsr['task_status'] = 'recived'
        csv_path = task_args['source_file_path']
        csv_name = csv_path.replace('\\','/').split('/')[-1]

        # 创建任务目录
        os.chdir( '/'.join(csv_path.replace('\\','/').split('/')[:-1]))
        if csv_name.split('.')[0] in os.listdir():
            os.chdir(csv_name.split('.')[0])
        else:
            os.mkdir(csv_name.split('.')[0])
            os.chdir(csv_name.split('.')[0])

        shutil.copy(task_args['source_file_path'],'.')

        # ctl
        ctl_name = csv_name.split('.')[0] + '.ctl'
        with open(csv_name,'r',encoding='gbk') as f:
            title_line = f.readline()
        truncate = 'truncate' if task_args['truncate'] == '1' else ''
        
        # title = [l.replace('\n','') for l in title_line.split(',')]
        # _column_str = ''
        # for t in title:
        #     _column_str += t + '  ' + 'char(200)' +',\n'
        # column_str = _column_str[:-2]
        db = Oradb(task_args['target_container'])
        columns_lst= db.columns(task_args['target_table'])
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
        '''.format(csv_name,task_args['target_table'],truncate,column_str)
        with open(ctl_name,'w+',encoding='utf-8') as ctl_f:
            ctl_f.write(ctl_content)

        # bat
        bat_name = csv_name.split('.')[0] + '.bat'
        userid = self.user_id[task_args['target_container']]
        bat_content = '''
        sqlldr userid={0} control={1} log={2} bad={3}
        '''.format(userid,ctl_name,csv_name.split('.')[0] + '.log',csv_name.split('.')[0] + '.bad')

        with open(bat_name, 'w+', encoding='utf-8') as bat_f:
            bat_f.write(bat_content)

        return  os.getcwd(),bat_name

    def doBat(self,task_args):
        now_path,bat_name = self.getFilesReady(task_args)
        p = Popen(bat_name,stdout=PIPE,stderr=PIPE)
        while p.poll() is None :
            count_now=p.stdout.readline().decode('cp936').split(' ')[-1]
            return count_now
        return bat_name



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

    test = TaskProcesser()
    test.doBat(task_args)
