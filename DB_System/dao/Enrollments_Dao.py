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
    def students_enroll():#ѧ��ѡ��
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        while True:
            StudentID=input("������ѧ��").strip()
            if StudentID:
                cursor.execute("SELECT 1 FROM Students WHERE StudentID=%s"(StudentID))
                if not cursor.fatchone():
                    print("ѧ�Ų����ڣ�����������")
                else:
                    break
            else:
                print("ѧ�Ų���Ϊ�գ�����������")
        #��ѡ�γ���ͼ
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
        







