from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Courses_Dao:
    @staticmethod
    def add_courses(CourseName,Credit,TeacherID):#新增课程
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("INSERT INTO Courses (CourseName,Credit,TeacherID) VALUES(%s,%s,%s)"(CourseName,Credit,TeacherID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_name(newCourseName,CourseID):#编辑课程名称
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET CourseName=%s WHERE CourseID=%s"(newCourseName,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_credit(newCredit,CourseID):#编辑课程学分
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET Credit=%s WHERE CourseID=%s"(newCredit,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_teachers(newTeacherID,CourseID):#编辑授课教师
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET TeacherID=%s WHERE CourseID=%s"(newTeacherID,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def attach_course_tb(CourseID,TextbookID):#为课程绑定教材
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Textbooks SET CourseID=%s WHERE TextbookID=%s"(CourseID,TextbookID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def course_time_arr(CourseID,Day,StartTime,EndTime):#排课
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE TABLE SET Day=%s,StartTime=%s,EndTime=%s WHERE CourseID=%s ",(Day,StartTime,EndTime,CourseID,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()