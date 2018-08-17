import cx_Oracle

conn = cx_Oracle.connect('mk/mk@wtbzdb1')
cursor = conn.cursor()
sql = """CREATE TABLE FDSAF
(局向    varchar2(100),
责任人    varchar2(100),
综调账号    varchar2(100),
编码    varchar2(100))"""

cursor.execute(sql)