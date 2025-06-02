from numpy import False_
from dao.Courses_Dao import Courses_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
import datetime
import re
class Course_Services:
    @staticmethod
    def add_courses(CourseName,Credit,TeacherID):#�����γ�
        try:
            if not TeacherID or not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                return False,"��ʦID����Ϊ�ջ�ý�ʦ�����ڣ�����������"
            Courses_Dao.add_courses(CourseName,Credit,TeacherID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def edit_courses_name(CourseID,newCourseName):#�༭�γ�����
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"�ÿγ̲����ڣ�����������"
            Courses_Dao.edit_courses_name(newCourseName,CourseID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def edit_courses_credit(CourseID,newCredit):#�༭�γ�ѧ��
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"�ÿγ̲����ڣ�����������"
            Courses_Dao.edit_courses_credit()
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def edit_teachers(CourseID,newTeacherID):#�༭�ڿν�ʦ
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"�ÿγ̲����ڣ�����������"
            if not Search_Dao.search1('Teachers','TeacherID',newTeacherID):
                return False,"�ý�ʦ�����ڣ�����������"
            Courses_Dao.edit_teachers(newTeacherID,CourseID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def attach_course_tb(TextbookID,CourseID):#Ϊ�γ̰󶨽̲�
        try:
            if not Search_Dao.search1('Textbooks','TextbookID',TextbookID):
                return False,"�ý̲Ĳ����ڣ�����������"
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"�ÿγ̲����ڣ�����������"
            Courses_Dao.attach_course_tb(CourseID,TextbookID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def course_capacity(current_page):#�γ�������� ʵʱ��ʾѡ��������γ�������� Ԥ���������
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
        base_sql="""SELECT
                        CourseID,
                        CourseName,
                        Capacity,
                        remain
                        FROM vw_Course_Capacity
                        LIMIT %s OFFSET %s
        """
        count_sql="""SELECT COUNT(*) AS total FROM vw_Course_Capacity"""
        #��ҳ����
        page_size=20
        try:
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)
            #��ʾ����׼��
               
            #(��ʾ�߼�����)
            for item in results['data']:
                    capacity=item['Capacity']
                    remain=item['remain']
                        #״̬
                    item['status']="����"
                    if (remain/capacity>=0.9):
                        item['status']="Ԥ����"
            return True,results
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def course_time_arr(CourseID,Day,StartTime,EndTime):#�ſ�
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"�ÿγ̲����ڣ�����������"
            if Search_Dao.search_time('Courses',Day,StartTime,EndTime):
                return False,"�����ſ�ʱ���ͻ���������ſ�"
            Courses_Dao.course_time_arr(CourseID,Day,StartTime,EndTime)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
