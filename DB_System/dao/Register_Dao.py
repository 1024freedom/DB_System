from sqlite3 import Cursor
from tkinter import TRUE
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
from utils.Security_tools import Security_tools
import pandas as pd
import re
import datetime
class Register_Dao():
    @staticmethod
    def register_student(user_id,password):#ע��ѧ���û�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        role='ѧ��'
        password=Security_tools.hash_password(password)#��ϣ���ܴ洢
        try:
            cursor.execute("INSERT INTO UserRoles(UserID,Role,Password) VALUES(%s,%s,%s)",(user_id,role,password,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def register_teacher(user_id,password):#ע���ʦ�û�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        role='��ʦ'
        password=Security_tools.hash_password(password)
        try:
            cursor.execute("INSERT INTO UserRoles(UserID,Role,Password) VALUES(%s,%s,%s)",(user_id,role,password,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()