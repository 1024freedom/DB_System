from dao.Enrollments_Dao import Enrollments_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
import datetime
import re
class Enrollments_Servises:
    @staticmethod
    def students_enroll_avail(current_page):#可选课程查询
        #可选课程视图（处理课程余量)
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
            #显示数据准备
               
            #(显示逻辑处理)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def students_drop_course():#学生退课
        while True:
            StudentID=input("请输入学号").strip()
            if StudentID:
                if not Search_Dao.search1('Enrollments','StudentID',StudentID):
                    print("选课记录中不存在该学号，请重新输入")
                else:
                    break
            else:
                print("学号不能为空，请重新输入")
        while True:
            CourseID=input("请输入要退选的课程ID").strip()
            if CourseID:
                if not Search_Dao.search2('Enrollments','StudentID','CourseID',StudentID,CourseID):
                    print("选课记录中不存在该课程，请重新输入")
                else:
                    break
            else:
                print("课程号不能为空，请重新输入")
        try:
            Enrollments_Dao.students_drop_course(StudentID,CourseID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def students_enroll_ask(current_page,ID):#学生选课记录查询
        #选课记录视图
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
            #显示数据准备
               
            #(显示逻辑处理)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            print(f"操作失败：{str(e)}")


