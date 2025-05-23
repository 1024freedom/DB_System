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
        #��ѡ�γ���ͼ������γ�����)
                """CREATE VIEW AvailableCourses AS
                SELECT
                    c.CourseID,
                    c.CourseName,
                    c.Credit,
                    t.Name,
                    c.Day,
                    c.StartTime,
                    c.EndTime,
                    (c.Capacity-COUNT(e.EnrollmentID)) AS remain
                FROM Courses c
                LEFT JOIN Enrollments e ON c.CourseID=e.CourseID
                LEFT JOIN Teachers t ON c.TeacherID=t.TeacherID
                GROUP BY c.CourseID
                HAVING remain>0
        """
            cursor.execute("""SELECT 
                                CourseID,
                                CourseName,
                                Credit,
                                Name,
                                Day,
                                StartTime,
                                EndTime,
                                remain
                            FROM AvailableCourses
            """)
            available_courses=cursor.fetchall()
            if not available_courses:
                print("û�п�ѡ�γ�")
                return
            #��ӡ��ѡ�γ�
            #�γ�ID �γ����� ѧ�� �ڿν�ʦ ���� �Ͽ�ʱ�� �¿�ʱ�� ����
            print("��ѡ�γ�:")
            print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(
                "�γ�ID", "�γ�����", "�ڿν�ʦ", "����", "�Ͽ�ʱ��", "�¿�ʱ��", "����"))
            for course in available_courses:
                print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(*course))

            #ѡ��γ�
            while True:
                while True:
                    CourseID=input("������Ҫѡ��Ŀγ�ID(����q�˳�)").strip()
                    if CourseID.lower()=='q':
                        return
                    cursor.execute("SELECT 1 FROM AvailableCourses WHERE CourseID=%s"(CourseID))
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
    def students_drop_course():#ѧ���˿�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            StudentID=input("������ѧ��").strip()
            if StudentID:
                cursor.execute("SELECT 1 FROM Enrollments WHERE StudentID=%s"(StudentID))
                if not cursor.fatchone():
                    print("ѡ�μ�¼�в����ڸ�ѧ�ţ�����������")
                else:
                    break
            else:
                print("ѧ�Ų���Ϊ�գ�����������")
        while True:
            CourseID=input("������Ҫ��ѡ�Ŀγ�ID").strip()
            if CourseID:
                cursor.execute("SELECT 1 FROM Enrollments WHERE StudentID=%s ADD CourseID=%s"(StudentID,CourseID))
                if not cursor.fatchone():
                    print("ѡ�μ�¼�в����ڸÿγ̣�����������")
                else:
                    break
            else:
                print("�γ̺Ų���Ϊ�գ�����������")
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
    def students_enroll_ask()#ѡ�μ�¼��ѯ
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        #ѡ�μ�¼��ͼ
        """CREATE VIEW StudentEnrollments AS 
         SELECT 
            e.EnrollmentID,
            s.StudentID,
            s.Name AS StudentName,
            c.CourseID,
            c.CourseName,
            t.Name AS TeacherName,
            c.Day,
            c.StartTime,
            c.EndTime
        FROM Enrollments e
        LEFT JOIN Students s ON e.StudentID=s.StudentID
        LEFT JOIN Courses c ON e.CourseID=c.CourseID
        LEFT JOIN Teachers t ON c.TeacherID=t.TeacherID
        """
        







