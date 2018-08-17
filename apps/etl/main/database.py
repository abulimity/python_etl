# coding=utf-8
# author = abulimity
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_etl.settings")
django.setup()
from apps.etl.models import DataContainer
import cx_Oracle

class Oradb:

    def __init__(self,db_id):
        self.db_id = db_id
        self.db_info = None
        self.conn = None
        self.cursor = None
        self.__getConn()


    def __getConn(self):
        try:
            self.db_info = DataContainer.objects.get(id=self.db_id)
        except DataContainer.DoesNotExist as e:
            print('Given database container named "%s" do not exist:  %s' %(self.db_name,e))
        except DataContainer.MultipleObjectsReturned as e:
            print('More than one database containers named "%s" ware found:  %s' %(self.db_name,e))
        else:
            try:
                print(self.db_info.user_id,self.db_info.pass_word,'{0}:{1}/{2}'.format(self.db_info.ip,self.db_info.port,self.db_info.service_name))
                conn = cx_Oracle.connect(self.db_info.user_id,self.db_info.pass_word,
                                                                                    '{0}:{1}/{2}'.format(self.db_info.ip,
                                                                                                         self.db_info.port,
                                                                                                         self.db_info.service_name))
            except Exception as e:
                print(e)
            else:
                cursor = conn.cursor()
                print('test successed:%s'%conn.version)
                self.conn = conn
                self.cursor = cursor


    def close(self):
        # self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def excute(self,sql,args = {}):
        try:
            return self.cursor.execute(sql, args)
        except Exception as e:
            print("Excute sql error:  %s"% e)
            self.close()

    #提取数据，参数一提取的记录数，参数二，是否以字典方式提取。为true时返回：{'字段1':'值1','字段2':'值2'}
    def get_rows(self, size = None,is_dict = True):
        if size is None:
            rows = self.cursor.fetchall()
        else:
            rows = self.cursor.fetchmany(size)
        if rows is None:
            rows=[]
        if is_dict:
            dict_rows=[]
            dict_keys = [r[0] for r in self.cursor.description ]
            for row in rows:
                dict_rows.append(dict(zip(dict_keys,row)))
            rows = dict_rows
        return rows


    def query(self,sql,args = {},size = None,is_dict = True):
        self.excute(sql,args)
        return self.get_rows(size,is_dict)

    def columns(self,table):
        sql = """SELECT T1.COLUMN_NAME,T1.DATA_TYPE,T1.DATA_LENGTH FROM USER_TAB_COLUMNS T1 WHERE T1.TABLE_NAME = :tablename"""
        args = {'tablename':table.upper()}
        self.excute(sql,args)
        return self.get_rows()

    def checkTable(self,table):
        sql = """SELECT COUNT(*) FROM USER_TABLES T1 WHERE T1.TABLE_NAME = :tablename"""
        args = {'tablename':table.upper()}
        self.excute(sql,args)
        return self.get_rows(is_dict=False)

    def countTable(self,table):
        sql = """SELECT COUNT(*) FROM {0}""".format(table.upper())
        self.excute(sql)
        return self.get_rows(is_dict=False)

    def truncateTable(self,table):
        sql = """TRUNCATE TABLE {0}""".format(table.upper())
        self.excute(sql)




if __name__ == '__main__':
    test = Oradb('mk')
    print(test.checkTable('pyhotn_etl_test1'))
