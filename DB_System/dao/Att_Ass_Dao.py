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
    def Attendance_add(StudentID,CourseID,Date,Status):#考勤记录
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("INSERT INTO Attendance (StudentID,CourseID,Date,Status) VALUES (%s,%s,%s,%s)"(StudentID,CourseID,Date,Status))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def Assignment_add(CourseID,Title,Deadline):#作业发布
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("INSERT INTO Assignmnets (CourseID,Title,Deadline) VALUES (%s,%s,%s)"(CourseID,Title,Deadline))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()  
    
