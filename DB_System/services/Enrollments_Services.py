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
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def students_drop_course():#ѧ���˿�
        while True:
            StudentID=input("������ѧ��").strip()
            if StudentID:
                if not Search_Dao.search1('Enrollments','StudentID',StudentID):
                    print("ѡ�μ�¼�в����ڸ�ѧ�ţ�����������")
                else:
                    break
            else:
                print("ѧ�Ų���Ϊ�գ�����������")
        while True:
            CourseID=input("������Ҫ��ѡ�Ŀγ�ID").strip()
            if CourseID:
                if not Search_Dao.search2('Enrollments','StudentID','CourseID',StudentID,CourseID):
                    print("ѡ�μ�¼�в����ڸÿγ̣�����������")
                else:
                    break
            else:
                print("�γ̺Ų���Ϊ�գ�����������")
        try:
            Enrollments_Dao.students_drop_course(StudentID,CourseID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
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
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page,ID)
            #��ʾ����׼��
               
            #(��ʾ�߼�����)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")


