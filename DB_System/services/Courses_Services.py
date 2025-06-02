from numpy import False_
from dao.Courses_Dao import Courses_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
import datetime
import re
class Course_Services:
    @staticmethod
    def add_courses(CourseName,Credit,TeacherID):#新增课程
        try:
            if not TeacherID or not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                return False,"教师ID不能为空或该教师不存在，请重新输入"
            Courses_Dao.add_courses(CourseName,Credit,TeacherID)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def edit_courses_name(CourseID,newCourseName):#编辑课程名称
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"该课程不存在，请重新输入"
            Courses_Dao.edit_courses_name(newCourseName,CourseID)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def edit_courses_credit(CourseID,newCredit):#编辑课程学分
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"该课程不存在，请重新输入"
            Courses_Dao.edit_courses_credit()
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def edit_teachers(CourseID,newTeacherID):#编辑授课教师
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"该课程不存在，请重新输入"
            if not Search_Dao.search1('Teachers','TeacherID',newTeacherID):
                return False,"该教师不存在，请重新输入"
            Courses_Dao.edit_teachers(newTeacherID,CourseID)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def attach_course_tb(TextbookID,CourseID):#为课程绑定教材
        try:
            if not Search_Dao.search1('Textbooks','TextbookID',TextbookID):
                return False,"该教材不存在，请重新输入"
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"该课程不存在，请重新输入"
            Courses_Dao.attach_course_tb(CourseID,TextbookID)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def course_capacity(current_page):#课程容量监控 实时显示选课人数与课程最大容量 预警超限情况
        #容量监控视图
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
        #分页参数
        page_size=20
        try:
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)
            #显示数据准备
               
            #(显示逻辑处理)
            for item in results['data']:
                    capacity=item['Capacity']
                    remain=item['remain']
                        #状态
                    item['status']="正常"
                    if (remain/capacity>=0.9):
                        item['status']="预警！"
            return True,results
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def course_time_arr(CourseID,Day,StartTime,EndTime):#排课
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"该课程不存在，请重新输入"
            if Search_Dao.search_time('Courses',Day,StartTime,EndTime):
                return False,"与已排课时间冲突，请重新排课"
            Courses_Dao.course_time_arr(CourseID,Day,StartTime,EndTime)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
