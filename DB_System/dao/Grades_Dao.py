from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Grades_Dao:
    def grades_insert_once():#单条成绩录入
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
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
            Score=input("请输入要录取的成绩分数(0~100):")
            if Score>100 or Score<0:
                print("输入的成绩不合法,请重新输入")
            else:
                break
        try:
            cursor.execute("INSERT INTO Grades (StudentID,CourseID,Score) VALUES (%s,%s,%s)"(StudentID,CourseID,Score))
            conn.commit()
            print("录入成功")
        except Exception as e:
            conn.rollback()
            print(f"录入失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()





