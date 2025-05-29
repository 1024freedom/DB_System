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
            #选择课程
            while True:
                while True:
                    CourseID=input("请输入要选择的课程ID(输入q退出)").strip()
                    if CourseID.lower()=='q':
                        return
                    cursor.execute("SELECT 1 FROM vw_Available_Courses WHERE CourseID=%s"(CourseID))
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
    @staticmethod
    def students_drop_course(StudentID,CourseID):#学生退课
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
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
    
        







