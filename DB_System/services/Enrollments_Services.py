from numpy import False_
from sqlalchemy import false
from dao.Enrollments_Dao import Enrollments_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
import datetime
import re
class Enrollments_Servises:
    @staticmethod
    def students_enroll_avail(current_page):#��ѡ�γ̲�ѯ
        #��ѡ�γ���ͼ������γ�����)
        """CREATE VIEW vw_Available_Courses AS
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
        base_sql="""SELECT 
                        CourseID,
                        CourseName,
                        Credit,
                        Name,
                        Day,
                        StartTime,
                        EndTime,
                        remain
                    FROM vw_Available_Courses
        """
        count_sql="""SELECT COUNT(*) AS total FROM  vw_Available_Courses
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
    @staticmethod
    def students_drop_course(StudentID,CourseID):#ѧ���˿�
        try:
            if not Search_Dao.search1('Enrollments','StudentID',StudentID):
                return False,"ѡ�μ�¼�в����ڸ�ѧ�ţ�����������"
            if not Search_Dao.search2('Enrollments','StudentID','CourseID',StudentID,CourseID):
                return False,"ѡ�μ�¼�в����ڸÿγ̣�����������"
            Enrollments_Dao.students_drop_course(StudentID,CourseID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def students_enroll_ask(current_page,ID):#ѧ��ѡ�μ�¼��ѯ
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
                        EnrollmentID,
                        StudentID,
                        StudentName,
                        CourseID,
                        CourseName,
                        TeacherName,
                        Day,
                        StartTime,
                        EndTime
                        FROM vw_Student_Enrollments
                        WHERE StudentID=%s
                        LIMIT %s OFFSET %s
        """
        count_sql="""SELECT COUNT(*) AS total FROM vw_Student_Enrollments 
        """
        page_size=20
        try:
            if not Search_Dao.search1('Students','StudentID',ID):
                    return False,"ѧ�Ų����ڣ�����������"
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page,ID)
            #��ʾ����׼��
               
            #(��ʾ�߼�����)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def students_enroll(StudentID,CourseID):#ѧ��ѡ��
       try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"ѧ�Ų����ڣ�����������"
            if not Search_Dao.search1('vw_Available_Courses','CourseID',CourseID):
                return False,"����Ŀγ�ID�����ڻ�ÿγ���������"
            else:
                if Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                    return False,"�ÿγ����Ѵ�������ѡ�α��У�����������" 
                #��ȡĿ��γ�ʱ���
                sql="""SELECT 
                        Day,StartTime ,EndTime 
                        FROM Courses WHERE CourseID=%s"""
                params=(CourseID,)
                course_time=Fetch_Dao.fetchof(sql,params)
                day,start,end=course_time[0]
            #��ȡ��ѡ�γ�ʱ���
                sql="""SELECT    
                        c.Day,
                        c.StartTime,
                        c.EndTime 
                        FROM Enrollments e JOIN Courses c
                        ON e.CourseID=c.CourseID
                        WHERE e.StudentID=%s
                    """
                params=(StudentID,)
                for(exist_day,exist_start,exist_end) in Fetch_Dao.fetchof(sql,params):
                    if day==exist_day:
                        if (start>exist_start and start<exist_end) or (end>exist_start and end<exist_end):
                            return False,"����ѡ��ʱ���ͻ��������ѡ��"
            
                Enrollments_Dao.students_enroll(StudentID,CourseID)
                return True,"�����ɹ�"
       except Exception as e:
          return False,f"{str(e)}"
