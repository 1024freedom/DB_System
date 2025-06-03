from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Grades_Dao:
    @staticmethod
    def grades_insert_once(StudentID,CourseID,Score):#单条成绩录入
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Grades (StudentID,CourseID,Score) VALUES (%s,%s,%s)"(StudentID,CourseID,Score))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    





