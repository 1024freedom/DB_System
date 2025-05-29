from dao.Courses_Dao import Courses_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
import datetime
import re
class Course_Services:
    @staticmethod
    def add_courses():#新增课程
        while True:
            CourseName=input("请输入课程名称").strip()
            if CourseName:
                break
            print("课程名不能为空，请重新输入")
        while True:
            Credit=input("请输入该课程的学分").strip()
            if Credit:
                break
            print("不能为空，请重新输入")
        while True:
            TeacherID=input("请输入授课教师ID").strip()
            if not TeacherID or not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                print("输入不能为空或该教师不存在，请重新输入")
            else:
                break
        try:
            Courses_Dao.add_courses(CourseName,Credit,TeacherID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def edit_courses_name():#编辑课程名称
        while True:
            CourseID=input("请输入要操作的课程ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
                print("课程ID不能为空或该课程不存在，请重新输入")
            else:
                break
        while True:
            newCourseName=input("请输入新名称").strip()
            if newCourseName:
                break
            else:
                print("课程名不能为空，请重新输入")
        try:
            Courses_Dao.edit_courses_name(newCourseName,CourseID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def edit_courses_credit():#编辑课程学分
        while True:
            CourseID=input("请输入要操作的课程ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
                print("课程ID不能为空或该课程不存在，请重新输入")
            else:
                break
        while True:
            newCredit=input("请输入学分").strip()
            if newCredit:
                break
            else:
                print("课程名不能为空，请重新输入")
        try:
            Courses_Dao.edit_courses_credit()
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def edit_teachers():#编辑授课教师
        while True:
            CourseID=input("请输入要操作的课程ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
                print("课程ID不能为空或该课程不存在，请重新输入")
            else:
                break
        while True:
            newTeacherID=input("请输入教师ID").strip()
            if newTeacherID:
                break
            else:
                print("ID不能为空，请重新输入")
        try:
            Courses_Dao.edit_teachers(newTeacherID,CourseID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def attach_course_tb():#为课程绑定教材
        while True:
            TextbookID=input("请输入要操作的教材ID").strip()
            if not TextbookID or not Search_Dao.search1('Textbooks','TextbookID',TextbookID):
                print("教材ID不能为空或该教材不存在，请重新输入")
            else:
                break
        while True:
            CourseID=input("请输入要绑定的课程ID").strip()
            if not CourseID or not Search_Dao.search1('Courses','CourseID',CourseID)
                print("课程ID不能为空或该课程不存在，请重新输入")
            else:
                break
        try:
            Courses_Dao.attach_course_tb(CourseID,TextbookID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
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
                    if remain/capacity>=0.9:
                        item['status']="预警！"
            return True,results
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def course_time_arr():#排课
        while True:
            CourseID=input("请输入要操作的课程ID")
            if CourseID:
                if Search_Dao.search1('Courses','CourseID',CourseID):
                    break
                else:
                    print("该课程不存在，请重新输入")
            else:
                print("课程ID不能为空，请重新输入")
        while True:
            Day=input("请输入上课的星期（1-7）")
            if Day:
                if 1<=Day<=7:
                    break
                else:
                    print("请输入数字1-7")
            else:
                print("星期不能为空，请重新输入")
        while True:
            StartTime=input("请输入上课时间")
            EndTime=input("请输入下课时间")
            if StartTime and EndTime:
                if Search_Dao.search_time('Courses',Day,StartTime,EndTime):
                    print("与已排课时间冲突，请重新排课")
                else:
                    break
            else:
                print("输入不能为空，请重新输入")
        try:
            Courses_Dao.course_time_arr(CourseID,Day,StartTime,EndTime)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
