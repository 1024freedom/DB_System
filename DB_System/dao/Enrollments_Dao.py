from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Enrollments_Dao:
    @staticmethod
    def students_enroll(StudentID,CourseID):#ѧ��ѡ��
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
                #д��ѡ�α�
        try:
            cursor.execute("INSERT INTO Enrollments (StudentID,CourseID) VALUES (%s,%s)"(StudentID,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def students_drop_course(StudentID,CourseID):#ѧ���˿�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        #���ļ�¼
        try:
            cursor.execute("DELETE FROM Enrollments WHERE StudentId=%s ADD CourseID=%s"(StudentID,CourseID))
            conn.commit()
            print("�˿γɹ�")
        except Exception as e:
            conn.rollback()
            print(f"����ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    
        







