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
    def add_courses():#�����γ�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            CourseName=input("������γ�����").strip()
            if CourseName:
                break
            print("�γ�������Ϊ�գ�����������")
        while True:
            Credit=input("������ÿγ̵�ѧ��").strip()
            if Credit:
                break
            print("����Ϊ�գ�����������")
        while True:
            TeacherID=input("�������ڿν�ʦID").strip()
            cursor.execute("SELECT 1 FROM Teachers WHERE TeacherID=%s"(TeacherID))
            if not TeacherID or not cursor.hatchone :
                print("���벻��Ϊ�ջ�ý�ʦ�����ڣ�����������")
            else:
                break
        try:
            cursor.execute("INSERT INTO Courses (CourseName,Credit,TeacherID) VALUES(%s,%s,%s)"(CourseName,Credit,TeacherID))
            conn.commit()
            print(f"�γ� '{CourseName}' �ѳɹ���ӣ�")
        except Exception as e:
            conn.rollback()
            print(f"��ӿγ�ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_name():#�༭�γ�����
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            CourseID=input("������Ҫ�����Ŀγ�ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
                print("�γ�ID����Ϊ�ջ�ÿγ̲����ڣ�����������")
            else:
                break
        while True:
            newCourseName=input("������������").strip()
            if newCourseName:
                break
            else:
                print("�γ�������Ϊ�գ�����������")
        try:
            cursor.execute("UPDATE FROM Courses SET CourseName=%s WHERE CourseID=%s"(newCourseName,CourseID))
            conn.commit()
            print(f"�༭�ɹ���")
        except Exception as e:
            conn.rollback()
            print(f"�༭ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_credit():#�༭�γ�ѧ��
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            CourseID=input("������Ҫ�����Ŀγ�ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
                print("�γ�ID����Ϊ�ջ�ÿγ̲����ڣ�����������")
            else:
                break
        while True:
            newCredit=input("������ѧ��").strip()
            if newCredit:
                break
            else:
                print("�γ�������Ϊ�գ�����������")
        try:
            cursor.execute("UPDATE FROM Courses SET Credit=%s WHERE CourseID=%s"(newCredit,CourseID))
            conn.commit()
            print(f"�༭�ɹ���")
        except Exception as e:
            conn.rollback()
            print(f"�༭ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_name():#�༭�ڿν�ʦ
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            CourseID=input("������Ҫ�����Ŀγ�ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
                print("�γ�ID����Ϊ�ջ�ÿγ̲����ڣ�����������")
            else:
                break
        while True:
            newTeacherID=input("�������ʦID").strip()
            if newTeacherID:
                break
            else:
                print("ID����Ϊ�գ�����������")
        try:
            cursor.execute("UPDATE FROM Courses SET TeacherID=%s WHERE CourseID=%s"(newTeacherID,CourseID))
            conn.commit()
            print(f"�༭�ɹ���")
        except Exception as e:
            conn.rollback()
            print(f"�༭ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def attach_course_tb():#Ϊ�γ̰󶨽̲�
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            TextbookID=input("������Ҫ�����Ľ̲�ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE TextbookID=%s"(TextbookID))
            if not TextbookID or not cursor.hatchone():
                print("�̲�ID����Ϊ�ջ�ý̲Ĳ����ڣ�����������")
            else:
                break
        while True:
            CourseID=input("������Ҫ�󶨵Ŀγ�ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
                print("�γ�ID����Ϊ�ջ�ÿγ̲����ڣ�����������")
            else:
                break
        try:
            cursor.execute("UPDATE FROM Textbooks SET CourseID=%s WHERE TextbookID=%s"(CourseID,TextbookID))
            conn.commit()
            print(f"�󶨳ɹ���")
        except Exception as e:
            conn.rollback()
            print(f"��ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def course_capacity():#�γ�������� ʵʱ��ʾѡ��������γ�������� Ԥ���������
        try:
            conn=DBPool.get_instance().get_conn()
            cursor=conn.cursor()
            #���������ͼ
            """CREATE VIEW CourseCapacity AS
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
            cursor.execute("SELECT COUNT(*) AS total FROM CourseCapacity ")
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
                                FROM CourseCapacity
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
            print(f"�γ�������ʾ�쳣��{str(e)}")
        finally:
            cursor.close()
            conn.close()
          
