from sqlite3 import Cursor
from openpyxl import Workbook
from utils.db_pool import DBPool

class Grades_Dao:
    @staticmethod
    def grades_insert_once(StudentID,CourseID,Score):#单条成绩录入
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Grades (StudentID,CourseID,Score) VALUES (%s,%s,%s)"(StudentID,CourseID,Score,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    





