from dao import Courses_Dao
from dao.Loans_Dao import Loans_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import date
import re
class Loans_Services:
    @staticmethod
    def equipments_loan():#设备借用
        while True:
            StudentID=input("请输入学生ID")
            if StudentID:
                if Search_Dao.search1('Students','StudentID',StudentID):
                    break
                else:
                    print("该学生不存在，请重新输入")
            else:
                print("学生ID不能为空，请重新输入")
        while True:
            EquipmentID=input("请输入设备ID")
            if EquipmentID:
                if (Search_Dao.search1('Equipments','EquipmentID',EquipmentID) 
                    and Fetch_Dao.fetch('Reserve','Equipments','EquipmentID',EquipmentID)>1):
                    break
                else:
                    print("该设备不存在或已无库存，请重新输入")
            else:
                print("设备ID不能为空，请重新输入")
        BorrowDate=date.today()
        pattern=r"^\d{4}-\d{2}-\d{2}$"#时间格式
        while True:
            ReturnDate=input("请输入归还日期 示例：2025-12-24")
            if ReturnDate:
                if not re.match(pattern,ReturnDate):
                    print("格式错误,请使用示例格式")
                else:
                    break
            else:
                print("归还日期不能为空，请输入")
        try:
            Loans_Dao.loan('Equipments','EquipmentLoans','EquipmentID',StudentID,EquipmentID,BorrowDate,ReturnDate)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def books_borrow():#图书借用
        while True:
            StudentID=input("请输入学生ID")
            if StudentID:
                if Search_Dao.search1('Students','StudentID',StudentID):
                    break
                else:
                    print("该学生不存在，请重新输入")
            else:
                print("学生ID不能为空，请重新输入")
        while True:
            BookID=input("请输入图书ID")
            if BookID:
                if (Search_Dao.search1('Books','BookID',BookID) 
                    and Fetch_Dao.fetch('Reserve','Books','BookID',BookID)>1):
                    break
                else:
                    print("该图书不存在或已无库存，请重新输入")
            else:
                print("图书ID不能为空，请重新输入")
        BorrowDate=date.today()
        pattern=r"^\d{4}-\d{2}-\d{2}$"#时间格式
        while True:
            ReturnDate=input("请输入归还日期 示例：2025-12-24")
            if ReturnDate:
                if not re.match(pattern,ReturnDate):
                    print("格式错误,请使用示例格式")
                else:
                    break
            else:
                print("归还日期不能为空，请输入")
        try:
            Loans_Dao.loan('Books','BookBorrows','BookID',StudentID,BookID,BorrowDate,ReturnDate)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")





