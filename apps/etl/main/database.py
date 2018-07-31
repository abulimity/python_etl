# # coding=utf-8
# # author = abulimity
# import cx_Oracle
#
#
# class Oradb:
#
#     def __init__(self,db_info=''):
#         self.db_config = {'7':'mk/mk@wtbzdb1',
#                               '8':'sjgl/Ju8THs_sj@SJGL_NEW'}
#         self.db_info = self.db_config.get(db_info,'')
#         self.conn,self.cursor = self.__getConn(db_info)
#
#
#     def __getConn(self,db_info):
#         if db_info.upper() in self.db_config:
#             try:
#                 conn = cx_Oracle.connect(self.db_config[db_info.upper()])
#             except Exception as e:
#                 print(e)
#             else:
#                 cursor = conn.cursor()
#                 return conn,cursor
#         else:
#             print('Wrong database info!')
#             return None,None
#
#     def close(self):
#         # self.conn.commit()
#         self.cursor.close()
#         self.conn.close()
#
#     def excute(self,sql,args = {}):
#         try:
#             return self.cursor.execute(sql, args)
#         except Exception as e:
#             self.close()
#             raise e
#
#     #提取数据，参数一提取的记录数，参数二，是否以字典方式提取。为true时返回：{'字段1':'值1','字段2':'值2'}
#     def get_rows(self, size = None,is_dict = True):
#         if size is None:
#             rows = self.cursor.fetchall()
#         else:
#             rows = self.cursor.fetchmany(size)
#         if rows is None:
#             rows=[]
#         if is_dict:
#             dict_rows=[]
#             dict_keys = [r[0] for r in self.cursor.description ]
#             for row in rows:
#                 dict_rows.append(dict(zip(dict_keys,row)))
#             rows = dict_rows
#         return rows
#
#
#     def query(self,sql,args = {},size = None,is_dict = True):
#         self.excute(sql,args)
#         return self.get_rows(size,is_dict)
#
#     def columns(self,table):
#         sql = """SELECT T1.COLUMN_NAME,T1.DATA_TYPE,T1.DATA_LENGTH FROM USER_TAB_COLUMNS T1 WHERE T1.TABLE_NAME = :tablename"""
#         args = {'tablename':table.upper()}
#         self.excute(sql,args)
#         return self.get_rows()
#
#     def checkTable(self,table):
#         sql = """SELECT COUNT(*) FROM USER_TABLES T1 WHERE T1.TABLE_NAME = :tablename"""
#         args = {'tablename':table.upper()}
#         self.excute(sql,args)
#         return self.get_rows(is_dict=False)
#
#
# if __name__ == '__main__':
#     test=Oradb('7')
#     print(test.conn.version)
#     test_sql = """profit_detail_107"""
#     print(test.checkTable('python_etl_test'))
#     test.close()