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
    def students_enroll():#ѧ��ѡ��
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            StudentID=input("������ѧ��").strip()
            if StudentID:
                cursor.execute("SELECT 1 FROM Students WHERE StudentID=%s"(StudentID))
                if not cursor.fatchone():
                    print("ѧ�Ų����ڣ�����������")
                else:
                    break
            else:
                print("ѧ�Ų���Ϊ�գ�����������")
            #ѡ��γ�
            while True:
                while True:
                    CourseID=input("������Ҫѡ��Ŀγ�ID(����q�˳�)").strip()
                    if CourseID.lower()=='q':
                        return
                    cursor.execute("SELECT 1 FROM vw_Available_Courses WHERE CourseID=%s"(CourseID))
                    if not cursor.fetchone():
                        print("����Ŀγ�ID�����ڻ�ÿγ���������")
                    else:
                        cursor.execute("SELECT 1 FROM Enrollments WHERE CourseID=%s AND StudentID=%s"(CourseID,StudentID))
                        if cursor.fetchone():
                            print("�ÿγ����Ѵ�������ѡ�α��У�����������")
                        else:
                            break
            #��ȡĿ��γ�ʱ���
                cursor.execute("SELECT Day,StartTime ,EndTime FROM Courses WHERE CourseID=%s"(CourseID))
                course_time=cursor.fetchone()
                day,start,end=course_time
            #��ȡ��ѡ�γ�ʱ���
                cursor.execute("""SELECT    
                                    c.Day,
                                    c.StartTime,
                                    c.EndTime 
                                    FROM Enrollments e JOIN Courses c
                                    ON e.CourseID=c.CourseID
                                    WHERE e.StudentID=%s
                                """(StudentID))
                exist=False
                for(exist_day,exist_start,exist_end) in cursor.fetchall():#����ʱ���ͻ
                    if day==exist_day:
                        if (start>exist_start and start<exist_end) or (end>exist_start and end<exist_end):
                            print("����ѡ��ʱ���ͻ��������ѡ��")
                            exist=True
                            break
                if exist:break
                #д��ѡ�α�
                try:
                    cursor.execute("INSERT INTO Enrollments (StudentID,CourseID) VALUES (%s,%s)"(StudentID,CourseID))
                    conn.commit()
                    print("�����ɹ�")
                except Exception as e:
                    conn.rollback()
                    print(f"����ʧ�ܣ�{str(e)}")
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
    
        







