from dao import Courses_Dao
from dao.Loans_Dao import Loans_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import date
import re
class Loans_Services:
    @staticmethod
    def equipments_loan():#�豸����
        while True:
            StudentID=input("������ѧ��ID")
            if StudentID:
                if Search_Dao.search1('Students','StudentID',StudentID):
                    break
                else:
                    print("��ѧ�������ڣ�����������")
            else:
                print("ѧ��ID����Ϊ�գ�����������")
        while True:
            EquipmentID=input("�������豸ID")
            if EquipmentID:
                if (Search_Dao.search1('Equipments','EquipmentID',EquipmentID) 
                    and Fetch_Dao.fetch('Reserve','Equipments','EquipmentID',EquipmentID)>1):
                    break
                else:
                    print("���豸�����ڻ����޿�棬����������")
            else:
                print("�豸ID����Ϊ�գ�����������")
        BorrowDate=date.today()
        pattern=r"^\d{4}-\d{2}-\d{2}$"#ʱ���ʽ
        while True:
            ReturnDate=input("������黹���� ʾ����2025-12-24")
            if ReturnDate:
                if not re.match(pattern,ReturnDate):
                    print("��ʽ����,��ʹ��ʾ����ʽ")
                else:
                    break
            else:
                print("�黹���ڲ���Ϊ�գ�������")
        try:
            Loans_Dao.loan('Equipments','EquipmentLoans','EquipmentID',StudentID,EquipmentID,BorrowDate,ReturnDate)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def books_borrow():#ͼ�����
        while True:
            StudentID=input("������ѧ��ID")
            if StudentID:
                if Search_Dao.search1('Students','StudentID',StudentID):
                    break
                else:
                    print("��ѧ�������ڣ�����������")
            else:
                print("ѧ��ID����Ϊ�գ�����������")
        while True:
            BookID=input("������ͼ��ID")
            if BookID:
                if (Search_Dao.search1('Books','BookID',BookID) 
                    and Fetch_Dao.fetch('Reserve','Books','BookID',BookID)>1):
                    break
                else:
                    print("��ͼ�鲻���ڻ����޿�棬����������")
            else:
                print("ͼ��ID����Ϊ�գ�����������")
        BorrowDate=date.today()
        pattern=r"^\d{4}-\d{2}-\d{2}$"#ʱ���ʽ
        while True:
            ReturnDate=input("������黹���� ʾ����2025-12-24")
            if ReturnDate:
                if not re.match(pattern,ReturnDate):
                    print("��ʽ����,��ʹ��ʾ����ʽ")
                else:
                    break
            else:
                print("�黹���ڲ���Ϊ�գ�������")
        try:
            Loans_Dao.loan('Books','BookBorrows','BookID',StudentID,BookID,BorrowDate,ReturnDate)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")





