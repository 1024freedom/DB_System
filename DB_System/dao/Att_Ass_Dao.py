from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
from datetime import date
class Att_Ass_Dao:
    @staticmethod
    def Attendance_add():#���ڼ�¼
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
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
            Status=input("����������Ŀ���״̬:").strip()
            if Status not in ('����','�ٵ�','ȱ��'):
                print("״̬���Ϸ�,����������")
            else:
                break
        Date=date.today()
        try:
            cursor.execute("INSERT INTO Attendance (StudentID,CourseID,Date,Status) VALUES (%s,%s,%s,%s)"(StudentID,CourseID,Date,Status))
            conn.commit()
            print("���ڼ�¼�ɹ�")
        except Exception as e:
            conn.rollback()
            print(f"���ڼ�¼ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def Assignment_add():#��ҵ����
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            CourseID=input("���������ҵ�����γ�ID")
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not cursor.fetchone():
                print("�ÿγ̲�����,����������")
            else:
                break
        while True:
            Title=input("��������ҵ����")
            if Title:
                break
            else:
                print("���ⲻ��Ϊ��")
        #�������ʱ��
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#ʱ���ʽ
        while True:
            Deadline=input("�������ύ��ֹʱ��(��ʽ:2025-12-31 23:34):").strip()
            if not Deadline:
                print("��ֹʱ�䲻��Ϊ��")
                continue
            if not re.match(pattern,Deadline):
                print("��ʽ����,��ʹ��ʾ����ʽ")
            else:
                break
        try:
            cursor.execute("INSERT INTO Assignmnets (CourseID,Title,Deadline) VALUES (%s,%s,%s)"(CourseID,Title,Deadline))
            conn.commit()
            print("��ҵ�����ɹ�")
        except Exception as e:
            conn.rollback()
            print(f"����ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()  

