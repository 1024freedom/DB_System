from dao import Courses_Dao 
from dao.Courses_Dao import Courses_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
class Course_Services:
    @staticmethod
    def add_courses():#�����γ�
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
            if not TeacherID or not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                print("���벻��Ϊ�ջ�ý�ʦ�����ڣ�����������")
            else:
                break
        try:
            Courses_Dao.add_courses(CourseName,Credit,TeacherID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def edit_courses_name():#�༭�γ�����
        while True:
            CourseID=input("������Ҫ�����Ŀγ�ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
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
            Courses_Dao.edit_courses_name(newCourseName,CourseID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def edit_courses_credit():#�༭�γ�ѧ��
        while True:
            CourseID=input("������Ҫ�����Ŀγ�ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
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
            Courses_Dao.edit_courses_credit()
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def edit_teachers():#�༭�ڿν�ʦ
        while True:
            CourseID=input("������Ҫ�����Ŀγ�ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
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
            Courses_Dao.edit_teachers(newTeacherID,CourseID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def attach_course_tb():#Ϊ�γ̰󶨽̲�
        while True:
            TextbookID=input("������Ҫ�����Ľ̲�ID").strip()
            if not TextbookID or not Search_Dao.search1('Textbooks','TextbookID',TextbookID):
                print("�̲�ID����Ϊ�ջ�ý̲Ĳ����ڣ�����������")
            else:
                break
        while True:
            CourseID=input("������Ҫ�󶨵Ŀγ�ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
                print("�γ�ID����Ϊ�ջ�ÿγ̲����ڣ�����������")
            else:
                break
        try:
            Courses_Dao.attach_course_tb(CourseID,TextbookID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def course_capacity():#�γ�������� ʵʱ��ʾѡ��������γ�������� Ԥ���������
        try:
            Courses_Dao.course_capacity()
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")

