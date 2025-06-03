from numpy import False_
from dao.LoanS_Dao import Loans_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import date
import re
class Loans_Services:
    @staticmethod
    def equipments_loan(StudentID,EquipmentID,ReturnDate):#设备借用
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"该学生不存在，请重新输入"
            if not (Search_Dao.search1('Equipments','EquipmentID',EquipmentID) 
                and Fetch_Dao.fetch('Reserve','Equipments','EquipmentID',EquipmentID)>1):
                return False,"该设备不存在或已无库存，请重新输入"
            BorrowDate=date.today()
            pattern=r"^\d{4}-\d{2}-\d{2}$"#时间格式
        
            if not re.match(pattern,ReturnDate):
                return False,"格式错误,请使用示例格式"
            Loans_Dao.loan('Equipments','EquipmentLoans','EquipmentID',StudentID,EquipmentID,BorrowDate,ReturnDate)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def books_borrow(StudentID,BookID,ReturnDate):#图书借用
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"该学生不存在，请重新输入"
            if not (Search_Dao.search1('Books','BookID',BookID) 
                and Fetch_Dao.fetch('Reserve','Books','BookID',BookID)>1):
                return False,"该图书不存在或已无库存，请重新输入"
            BorrowDate=date.today()
            pattern=r"^\d{4}-\d{2}-\d{2}$"#时间格式
            if not re.match(pattern,ReturnDate):
                return False,"格式错误,请使用示例格式"
            Loans_Dao.loan('Books','BookBorrows','BookID',StudentID,BookID,BorrowDate,ReturnDate)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"





