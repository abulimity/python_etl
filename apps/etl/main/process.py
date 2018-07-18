import os
import json


class TaskProcesser():

    def __init__(self):
        self.user_id = {
            'mk':'mk/mk@wtbzdb1',
            'sjgl':'sjgl/Ju8THs_sj@SJGL_NEW'
        }

    def take_task(self,task_argsr):
        # taskArgsr['task_status'] = 'recived'
        csv_path = task_argsr['source_file_path']
        csv_name = csv_path.replace('\\','/').split('/')[-1]
        # 创建任务目录
        os.chdir( '/'.join(csv_path.replace('\\','/').split('/')[:-1]))
        if csv_name.split('.')[0] in os.listdir():
            os.chdir(csv_name.split('.')[0])
        else:
            os.mkdir(csv_name.split('.')[0])
            os.chdir(csv_name.split('.')[0])
        # ctl
        ctl_name = csv_name.split('.')[0] + '.ctl'

        # bat
        bat_name = csv_name.split('.')[0] + '.bat'
        bat_f = open(bat_name,'w+',encoding='utf-8')
        if task_argsr['target_contain']=='7':
            userid = self.user_id['mk']
        bat_content = '''
        sqlldr userid={0} control={1} log={2} bad={3}
        '''
        bat_f.write(bat_content)

        return  os.getcwd()

    def create_csv(self):
        pass

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
        self.create_csv()
        csv_file.close()

        return json_dic

    def close(self,file):
        file.colse()
        return

if __name__ == '__main__':
    task_argsr = {'target_container': '7',
                  'task_status': 'recived',
                  'target_table': 'ddd',
                  'source_table': '', 'target_sql': '',
                  'source_file_path': 'E:\\project\\python_etl\\media\\upload\\etl\\杨哲_20180718170220.csv',
                  'user_name': '杨哲',
                  'truncate': '0',
                  'source_sql': '',
                  'source_container': '1'}

    test = TaskProcesser()
    print(test.taketask(task_argsr))
