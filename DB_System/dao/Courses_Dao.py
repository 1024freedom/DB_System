from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Courses_Dao:
    @staticmethod
    def add_courses(CourseName,Credit,TeacherID):#�����γ�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("INSERT INTO Courses (CourseName,Credit,TeacherID) VALUES(%s,%s,%s)"(CourseName,Credit,TeacherID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_name(newCourseName,CourseID):#�༭�γ�����
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET CourseName=%s WHERE CourseID=%s"(newCourseName,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_credit(newCredit,CourseID):#�༭�γ�ѧ��
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET Credit=%s WHERE CourseID=%s"(newCredit,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_teachers(newTeacherID,CourseID):#�༭�ڿν�ʦ
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET TeacherID=%s WHERE CourseID=%s"(newTeacherID,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def attach_course_tb(CourseID,TextbookID):#Ϊ�γ̰󶨽̲�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Textbooks SET CourseID=%s WHERE TextbookID=%s"(CourseID,TextbookID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def course_capacity():#�γ�������� ʵʱ��ʾѡ��������γ�������� Ԥ���������
        try:
            conn=DBPool.get_instance().get_conn()
            cursor=conn.cursor()
            #���������ͼ
            """CREATE VIEW vw_Course_Capacity AS
                SELECT
                  c.CourseID,
                  c.CourseName,
                  c.Capacity,
                  (c.Capacity-COUNT(e.EnrollmentID)) AS remain
                  FROM Courses c
                  LEFT JOIN Enrollments e ON c.CourseID=e.CourseID
                  GROUP BY c.CourseID
            """
            #��ȡ�ܼ�¼��
            cursor.execute("SELECT COUNT(*) AS total FROM vw_Course_Capacity ")
            total_records=cursor.fetchone()['total']
            if total_records==0:
                print("��ǰû������")
                return
            #���÷�ҳ����
            page_size=20#Ĭ��ÿҳ��ʾ20��
            total_pages=(total_records+page_size-1)//page_size#����ȡ��
            current_page=1
            while True:
                #����ƫ����
                offset=(current_page-1)*page_size
                #��ҳ��ѯ
                cursor.execute("""SELECT
                                CourseID,
                                CourseName,
                                Capacity,
                                remain
                                FROM vw_Course_Capacity
                                LIMIT %s OFFSET %s
                                """(page_size,offset))
                courses=cursor.fetchall()
                if not courses:
                    print("�޿γ�����")
                    return
                #��ʾ����׼��
                display_data=[]
               
                for course in courses:
                        capacity=course['Capacity']
                        remain=course['remain']
                        #״̬
                        status="����"
                        if remain/capacity>=0.9:
                            status="Ԥ����"
                        display_data.append({
                            'CourseID':course['CourseID'],
                            'CourseName':course['CourseName'],
                            'Capacity':course['Capacity'],
                            'remain':course['remain'],
                            'status':status
                            })
                    #��ӡ
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                        "�γ�ID","�γ�����","����","����","״̬"))
                print("-"*60)
                for item in display_data:
                        print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                            item['CourseID'],
                            item['CourseName'],
                            item['Capacity'],
                            item['remain'],
                            item['status']
                            ))
                    #��ҳ����
                if total_pages>1:
                        action=input("���������:n:��һҳ p:��һҳ j:��תĿ��ҳ q:�˳� ").lower()
                        if action=='n':
                            current_page=min(current_page+1,total_pages)
                        elif action=='p':
                            current_page=max(current_page-1,1)
                        elif action=='j':
                            target=int(input(f"������Ŀ��ҳ(1-{total_pages})"))
                            current_page=max(1,min(target,total_pages))
                        elif action=='q':
                            break
                        else:
                            print("��Ч������")
                else:
                        input("û�и���ҳ,�����������")
                        break

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def course_time_arr(CourseID,Day,StartTime,EndTime):#�ſ�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE TABLE SET Day=%s,StartTime=%s,EndTime=%s WHERE CourseID=%s ",(Day,StartTime,EndTime,CourseID,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()