from services.Loans_Services import Loans_Services
class Loans_cli:
    @staticmethod
    def show_menu():
        print("\n===== �ɼ�����ҳ�� =====")
        print("1. �豸����")
        print("2. ͼ�����")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def equipments_loan():#�豸����
        while True:
            while True:
                StudentID=input("������ѧ��ID")
                if StudentID:
                    break
                else:
                    print("ѧ��ID����Ϊ�գ�����������")
            while True:
                EquipmentID=input("�������豸ID")
                if EquipmentID:
                    break
                else:
                    print("�豸ID����Ϊ�գ�����������")
            while True:
                ReturnDate=input("������黹���� ʾ����2025-12-24")
                if ReturnDate:
                    break
                else:
                    print("�黹���ڲ���Ϊ�գ�������")
            success,message=Loans_Services.equipments_loan(StudentID,EquipmentID,ReturnDate)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def books_borrow():#ͼ�����
        while True:
            while True:
                StudentID=input("������ѧ��ID")
                if StudentID:
                    break
                else:
                    print("ѧ��ID����Ϊ�գ�����������")
            while True:
                BookID=input("������ͼ��ID")
                if BookID:
                    break
                else:
                    print("ͼ��ID����Ϊ�գ�����������")
            while True:
                ReturnDate=input("������黹���� ʾ����2025-12-24")
                if ReturnDate:
                    break
                else:
                    print("�黹���ڲ���Ϊ�գ�������")
            success,message=Loans_Services.books_borrow(StudentID,BookID,ReturnDate)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def run():
        Loans_cli.show_menu()
        choice=1
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Loans_cli.equipments_loan()
                case 2:
                    Loans_cli.books_borrow()
                