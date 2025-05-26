from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Loans_Dao:
    @staticmethod
    def loan(table:str,table_loan:str,loan_ID_column:str,StudentID,loanID:any,BorrowDate,ReturnDate):#…Ë±∏ΩË”√
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute(f"INSERT INTO {table_loan} (StudentID,{loan_ID_column},BorrowDate,ReturnDate) VALUES (%s,%s,%s,%s)",(StudentID,loanID,BorrowDate,ReturnDate,))
            cursor.execute(f"UPDATE {table} SET Reserve=Reserve-1 WHERE {loan_ID_column}=%s",(loanID,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()






