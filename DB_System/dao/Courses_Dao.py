from sqlite3 import Cursor
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Courses_Dao:
    @staticmethod
    def add_courses():#�����γ�
        conn=DBPool.get_instance().get_coon()
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
        conn=DBPool.get_instance().get_coon()
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
        conn=DBPool.get_instance().get_coon()
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
        conn=DBPool.get_instance().get_coon()
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
        conn=DBPool.get_instance().get_coon()
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
    

