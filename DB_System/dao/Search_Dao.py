from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Search_Dao:
    def search1(table:str,column:str,value:any):#检查是否存在(存在返回true)
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        sql=f"SELECT 1 FROM {table} WHERE {column}=%s"
        cursor.execute(sql,(value,))
        if cursor.fetchone():
            return True
        else:
            return False
        cursor.close
        conn.close
    def search2(table:str,column1:str,column2:str,value1:any,value2:any):#检查是否存在(存在返回true)
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        sql=f"SELECT 1 FROM {table} WHERE {column1}=%s ADD {column2}=%s"
        cursor.execute(sql,(value1,value2,))
        if cursor.fetchone():
            return True
        else:
            return False
        cursor.close
        conn.close



