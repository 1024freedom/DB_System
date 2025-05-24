from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Enrollments_Dao:
    @staticmethod
    def students_enroll():#学生选课
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            StudentID=input("请输入学号").strip()
            if StudentID:
                cursor.execute("SELECT 1 FROM Students WHERE StudentID=%s"(StudentID))
                if not cursor.fatchone():
                    print("学号不存在，请重新输入")
                else:
                    break
            else:
                print("学号不能为空，请重新输入")
        #可选课程视图（处理课程余量)
                """CREATE VIEW AvailableCourses AS
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
            cursor.execute("""SELECT 
                                CourseID,
                                CourseName,
                                Credit,
                                Name,
                                Day,
                                StartTime,
                                EndTime,
                                remain
                            FROM AvailableCourses
            """)
            available_courses=cursor.fetchall()
            if not available_courses:
                print("没有可选课程")
                return
            #打印可选课程
            #课程ID 课程名称 学分 授课教师 星期 上课时间 下课时间 余量
            print("可选课程:")
            print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(
                "课程ID", "课程名称", "授课教师", "星期", "上课时间", "下课时间", "余量"))
            for course in available_courses:
                print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(*course))

            #选择课程
            while True:
                while True:
                    CourseID=input("请输入要选择的课程ID(输入q退出)").strip()
                    if CourseID.lower()=='q':
                        return
                    cursor.execute("SELECT 1 FROM AvailableCourses WHERE CourseID=%s"(CourseID))
                    if not cursor.fetchone():
                        print("输入的课程ID不存在或该课程已无余量")
                    else:
                        cursor.execute("SELECT 1 FROM Enrollments WHERE CourseID=%s AND StudentID=%s"(CourseID,StudentID))
                        if cursor.fetchone():
                            print("该课程您已存在与已选课表中，请重新输入")
                        else:
                            break
            #获取目标课程时间段
                cursor.execute("SELECT Day,StartTime ,EndTime FROM Courses WHERE CourseID=%s"(CourseID))
                course_time=cursor.fetchone()
                day,start,end=course_time
            #获取已选课程时间段
                cursor.execute("""SELECT 
                                    c.Day,
                                    c.StartTime,
                                    c.EndTime 
                                    FROM Enrollments e JOIN Courses c
                                    ON e.CourseID=c.CourseID
                                    WHERE e.StudentID=%s
                                """(StudentID))
                exist=False
                for(exist_day,exist_start,exist_end) in cursor.fetchall():#检验时间冲突
                    if day==exist_day:
                        if (start>exist_start and start<exist_end) or (end>exist_start and end<exist_end):
                            print("与已选课时间冲突，请重新选择")
                            exist=True
                            break
                if exist:break
                #写入选课表
                try:
                    cursor.execute("INSERT INTO Enrollments (StudentID,CourseID) VALUES (%s,%s)"(StudentID,CourseID))
                    conn.commit()
                    print("操作成功")
                except Exception as e:
                    conn.rollback()
                    print(f"操作失败：{str(e)}")
                finally:
                    cursor.close()
                    conn.close()
    def students_drop_course():#学生退课
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            StudentID=input("请输入学号").strip()
            if StudentID:
                cursor.execute("SELECT 1 FROM Enrollments WHERE StudentID=%s"(StudentID))
                if not cursor.fatchone():
                    print("选课记录中不存在该学号，请重新输入")
                else:
                    break
            else:
                print("学号不能为空，请重新输入")
        while True:
            CourseID=input("请输入要退选的课程ID").strip()
            if CourseID:
                cursor.execute("SELECT 1 FROM Enrollments WHERE StudentID=%s ADD CourseID=%s"(StudentID,CourseID))
                if not cursor.fatchone():
                    print("选课记录中不存在该课程，请重新输入")
                else:
                    break
            else:
                print("课程号不能为空，请重新输入")
        #更改记录
        try:
            cursor.execute("DELETE FROM Enrollments WHERE StudentId=%s ADD CourseID=%s"(StudentID,CourseID))
            conn.commit()
            print("退课成功")
        except Exception as e:
            conn.rollback()
            print(f"操作失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def students_enroll_ask():#选课记录查询
        try:
            conn=DBPool.get_instance().get_conn()
            cursor=conn.cursor()
            #选课记录视图
            """CREATE VIEW StudentEnrollments AS 
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
            #获取总记录数
            cursor.execute("SELECT COUNT(*) AS total FROM StudentEnrollments ")
            total_records=cursor.fetchone()['total']
            if total_records==0:
                print("当前没有数据")
                return
            #设置分页参数
            page_size=20#默认每页显示20条
            total_pages=(total_records+page_size-1)//page_size#向上取整
            current_page=1
            while True:
                #计算偏移量
                offset=(current_page-1)*page_size
                #分页查询
                cursor.execute("""SELECT
                                EnrollmentID,
                                StudentID,
                                StudentName,
                                CourseID,
                                CourseName,
                                TeacherName,
                                Day,
                                StartTime,
                                EndTime
                                FROM StudentEnrollments
                                LIMIT %s OFFSET %s
                                """(page_size,offset))


                enrollments=cursor.fetchall()
                if not enrollments:
                    print("无选课记录")
                    return
                #显示数据准备
                display_data=[]
               
                for enrollment in enrollments:
                    
                        display_data.append({
                            'EnrollmentID':enrollment['EnrollmentID'],
                            'StudentID':enrollment['StudentID'],
                            'StudentName':enrollment['StudentName'],
                            'CourseID':enrollment['CourseID'],
                            'CourseName':enrollment['CourseName'],
                            'TeacherName':enrollment['TeacherName'],
                            'Day':enrollment['Day'],
                            'StartTime':enrollment['StartTime'],
                            'EndTime':enrollment['EndTime']
                            })
                    #打印
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                        "选课记录ID","学生ID","学生姓名","课程ID","课程名","授课教师","星期","上课时间","下课时间"))
                print("-"*95)
                for item in display_data:
                        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                            item['EnrollmentID'],
                            item['StudentID'],
                            item['StudentName'],
                            item['CourseID'],
                            item['CourseName'],
                            item['TeacherName'],
                            item['Day'],
                            item['StartTime'],
                            item['EndTime']
                            ))
                    #分页导航
                if total_pages>1:
                        action=input("请输入操作:n:下一页 p:下一页 j:跳转目标页 q:退出 ").lower()
                        if action=='n':
                            current_page=min(current_page+1,total_pages)
                        elif action=='p':
                            current_page=max(current_page-1,1)
                        elif action=='j':
                            target=int(input(f"请输入目标页(1-{total_pages})"))
                            current_page=max(1,min(target,total_pages))
                        elif action=='q':
                            break
                        else:
                            print("无效操作码")
                else:
                        input("没有更多页,按任意键返回")
                        break
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"操作失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
        







