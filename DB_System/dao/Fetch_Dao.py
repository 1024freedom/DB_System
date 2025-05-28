from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL, paramstyle
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
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
    def fetchof(sql:str ,params:tuple):#获取较复杂sql语句的多个select结果
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        cursor.execute(sql,params)
        result=cursor.fetchall()
        cursor.close()
        conn.close()
        return result
        



