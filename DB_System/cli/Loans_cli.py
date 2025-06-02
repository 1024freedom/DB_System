from services.Loans_Services import Loans_Services
class Loans_cli:
    @staticmethod
    def show_menu():
        print("\n===== 成绩管理页面 =====")
        print("1. 设备借用")
        print("2. 图书借用")
        print("========================")
    @staticmethod
    def equipments_loan():#设备借用
        while True:
            while True:
                StudentID=input("请输入学生ID")
                if StudentID:
                    break
                else:
                    print("学生ID不能为空，请重新输入")
            while True:
                EquipmentID=input("请输入设备ID")
                if EquipmentID:
                    break
                else:
                    print("设备ID不能为空，请重新输入")
            while True:
                ReturnDate=input("请输入归还日期 示例：2025-12-24")
                if ReturnDate:
                    break
                else:
                    print("归还日期不能为空，请输入")
            success,message=Loans_Services.equipments_loan(StudentID,EquipmentID,ReturnDate)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def books_borrow():#图书借用
        while True:
            while True:
                StudentID=input("请输入学生ID")
                if StudentID:
                    break
                else:
                    print("学生ID不能为空，请重新输入")
            while True:
                BookID=input("请输入图书ID")
                if BookID:
                    break
                else:
                    print("图书ID不能为空，请重新输入")
            while True:
                ReturnDate=input("请输入归还日期 示例：2025-12-24")
                if ReturnDate:
                    break
                else:
                    print("归还日期不能为空，请输入")
            success,message=Loans_Services.books_borrow(StudentID,BookID,ReturnDate)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本