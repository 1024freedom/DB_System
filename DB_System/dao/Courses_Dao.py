from sqlite3 import Cursor
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Courses_Dao:
    @staticmethod
    def add_courses():#新增课程
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
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
            cursor.execute("SELECT 1 FROM Teachers WHERE TeacherID=%s"(TeacherID))
            if not TeacherID or not cursor.hatchone :
                print("输入不能为空或该教师不存在，请重新输入")
            else:
                break
        try:
            cursor.execute("INSERT INTO Courses (CourseName,Credit,TeacherID) VALUES(%s,%s,%s)"(CourseName,Credit,TeacherID))
            conn.commit()
            print(f"课程 '{CourseName}' 已成功添加！")
        except Exception as e:
            conn.rollback()
            print(f"添加课程失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_name():#编辑课程名称
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            CourseID=input("请输入要操作的课程ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
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
            cursor.execute("UPDATE FROM Courses SET CourseName=%s WHERE CourseID=%s"(newCourseName,CourseID))
            conn.commit()
            print(f"编辑成功！")
        except Exception as e:
            conn.rollback()
            print(f"编辑失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_credit():#编辑课程学分
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            CourseID=input("请输入要操作的课程ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
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
            cursor.execute("UPDATE FROM Courses SET Credit=%s WHERE CourseID=%s"(newCredit,CourseID))
            conn.commit()
            print(f"编辑成功！")
        except Exception as e:
            conn.rollback()
            print(f"编辑失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_name():#编辑授课教师
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            CourseID=input("请输入要操作的课程ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
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
            cursor.execute("UPDATE FROM Courses SET TeacherID=%s WHERE CourseID=%s"(newTeacherID,CourseID))
            conn.commit()
            print(f"编辑成功！")
        except Exception as e:
            conn.rollback()
            print(f"编辑失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def attach_course_tb():#为课程绑定教材
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            TextbookID=input("请输入要操作的教材ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE TextbookID=%s"(TextbookID))
            if not TextbookID or not cursor.hatchone():
                print("教材ID不能为空或该教材不存在，请重新输入")
            else:
                break
        while True:
            CourseID=input("请输入要绑定的课程ID").strip()
            cursor.execute("SELECT 1 FROM Courses WHERE CourseID=%s"(CourseID))
            if not CourseID or not cursor.hatchone():
                print("课程ID不能为空或该课程不存在，请重新输入")
            else:
                break
        try:
            cursor.execute("UPDATE FROM Textbooks SET CourseID=%s WHERE TextbookID=%s"(CourseID,TextbookID))
            conn.commit()
            print(f"绑定成功！")
        except Exception as e:
            conn.rollback()
            print(f"绑定失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    

