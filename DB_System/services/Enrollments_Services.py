from dao.Enrollments_Dao import Enrollments_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
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
            return False,f"{str(e)}"
    @staticmethod
    def students_drop_course(StudentID,CourseID):#学生退课
        try:
            if not Search_Dao.search1('Enrollments','StudentID',StudentID):
                return False,"选课记录中不存在该学号，请重新输入"
            if not Search_Dao.search2('Enrollments','StudentID','CourseID',StudentID,CourseID):
                return False,"选课记录中不存在该课程，请重新输入"
            Enrollments_Dao.students_drop_course(StudentID,CourseID)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
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
            if not Search_Dao.search1('Students','StudentID',ID):
                    return False,"学号不存在，请重新输入"
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page,ID)
            #显示数据准备
               
            #(显示逻辑处理)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def students_enroll(StudentID,CourseID):#学生选课
       try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"学号不存在，请重新输入"
            if not Search_Dao.search1('vw_Available_Courses','CourseID',CourseID):
                return False,"输入的课程ID不存在或该课程已无余量"
            else:
                if Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                    return False,"该课程您已存在与已选课表中，请重新输入" 
                #获取目标课程时间段
                sql="""SELECT 
                        Day,StartTime ,EndTime 
                        FROM Courses WHERE CourseID=%s"""
                params=(CourseID,)
                course_time=Fetch_Dao.fetchof(sql,params)
                day,start,end=course_time[0]
            #获取已选课程时间段
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
                            return False,"与已选课时间冲突，请重新选择"
            
                Enrollments_Dao.students_enroll(StudentID,CourseID)
                return True,"操作成功"
       except Exception as e:
          return False,f"{str(e)}"
