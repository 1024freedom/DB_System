from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Grades_Dao:
    def grades_insert_once():#�����ɼ�¼��
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        while True:
            StudentID = input("������ѧ��ID��").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("��ѧ�������ڣ����������룺")
            else:
                break
        while True:
            CourseID = input("������γ�ID��").strip()
            cursor.execute("SELECT 1 FROM Enrollments WHERE CourseID = %s ADD StudentID=%s", (CourseID,StudentID))
            if not cursor.fetchone():
                print("�ÿγ̲����ڸ�ѧ���Ŀα��У����������룺")
            else:
                break
        while True:
            Score=input("������Ҫ¼ȡ�ĳɼ�����(0~100):")
            if Score>100 or Score<0:
                print("����ĳɼ����Ϸ�,����������")
            else:
                break
        try:
            cursor.execute("INSERT INTO Grades (StudentID,CourseID,Score) VALUES (%s,%s,%s)"(StudentID,CourseID,Score))
            conn.commit()
            print("¼��ɹ�")
        except Exception as e:
            conn.rollback()
            print(f"¼��ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()





