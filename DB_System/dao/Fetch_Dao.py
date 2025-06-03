from sqlite3 import Cursor
from utils.db_pool import DBPool
class Fetch_Dao:
    def fetch(fetch:str,table:str,column:str,value:any):
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        sql=f"SELECT {fetch} FROM {table} WHERE {column}=%s"
        cursor.execute(sql,(value,))
        fetchvalue=cursor.fetchone()
        cursor.close()
        conn.close()
        return fetchvalue
    def fetchas(fetch:str,fetchas:str,table:str,column:str,value:any):
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        sql=f"SELECT {fetch} AS {fetchas} FROM {table} WHERE {column}=%s"
        cursor.execute(sql,(value,))
        fetchvalue=cursor.fetchone()
        cursor.close()
        conn.close()
        return fetchvalue
    def fetchof(sql:str ,params:tuple):#直接获取sql语句的结果
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        if params:
            cursor.execute(sql,params)
        else:
            cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()
        conn.close()
        return result
        



