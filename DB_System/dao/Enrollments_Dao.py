from sqlite3 import Cursor
from openpyxl import Workbook
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Enrollments_Dao:
    @staticmethod
    def students_enroll(StudentID,CourseID):#学生选课
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
                #写入选课表
        try:
            cursor.execute("INSERT INTO Enrollments (StudentID,CourseID) VALUES (%s,%s)"(StudentID,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
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
    
        







