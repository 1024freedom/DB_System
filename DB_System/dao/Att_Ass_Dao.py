from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
from datetime import date
class Att_Ass_Dao:
    @staticmethod
    def Attendance_add():#考勤记录
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            StudentID = input("请输入学生ID：").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("该学生不存在，请重新输入：")
            else:
                break
        while True:
            CourseID = input("请输入课程ID：").strip()
            cursor.execute("SELECT 1 FROM Enrollments WHERE CourseID = %s ADD StudentID=%s", (CourseID,StudentID))
            if not cursor.fetchone():
                print("该课程不存在该学生的课表中，请重新输入：")
            else:
                break
        while True:
            Status=input("请输入该生的考勤状态:").strip()
            if Status not in ('出勤','迟到','缺勤'):
                print("状态不合法,请重新输入")
            else:
                break
        Date=date.today()
        try:
            cursor.execute("INSERT INTO Attendance (StudentID,CourseID,Date,Status) VALUES (%s,%s,%s,%s)"(StudentID,CourseID,Date,Status))
            conn.commit()
            print("考勤记录成功")
        except Exception as e:
            conn.rollback()
            print(f"考勤记录失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def Assignment_add():#作业发布
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            CourseID=input("请输入该作业关联课程ID")
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not cursor.fetchone():
                print("该课程不存在,请重新输入")
            else:
                break
        while True:
            Title=input("请输入作业标题")
            if Title:
                break
            else:
                print("标题不能为空")
        #处理截至时间
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#时间格式
        while True:
            Deadline=input("请输入提交截止时间(格式:2025-12-31 23:34):").strip()
            if not Deadline:
                print("截止时间不能为空")
                continue
            if not re.match(pattern,Deadline):
                print("格式错误,请使用示例格式")
            else:
                break
        try:
            cursor.execute("INSERT INTO Assignmnets (CourseID,Title,Deadline) VALUES (%s,%s,%s)"(CourseID,Title,Deadline))
            conn.commit()
            print("作业发布成功")
        except Exception as e:
            conn.rollback()
            print(f"发布失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()  

