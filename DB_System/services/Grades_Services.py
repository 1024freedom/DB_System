from pickle import FALSE
from numpy import False_
from sqlalchemy import false
from dao.Grades_Dao import Grades_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
import datetime
import re
class Grades_Services:
    @staticmethod
    def grades_insert_once(StudentID,CourseID,Score):#�����ɼ�¼��
        try:
            if not Search_Dao.search1('Studnets','StudentID',StudentID):
                return False,"��ѧ�������ڣ����������룺"
            if not Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                return False,"�ÿγ̲����ڸ�ѧ���Ŀα��У����������룺"
            Grades_Dao.grades_insert_once(StudentID,CourseID,Score)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def grades_alert(current_page):#���ɾ�������
        #ѡ�μ�¼��ͼ
        """CREATE VIEW vw_Student_Enrollments AS 
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
        base_sql="""SELECT
                        StudentID,
                        CourseID,
                        StudentName,
                        CourseName,
                        Score
                        FROM vw_Grades_Alert
                        LIMIT %s OFFSET %s
        """
        count_sql="""SELECT COUNT(*) AS total FROM vw_Grades_Alert 
        """
        page_size=20
        try:
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)
            #��ʾ����׼��
               
            #(��ʾ�߼�����)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            return False,f"{str(e)}"


