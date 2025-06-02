from services.Att_Ass_Services import Att_Ass_Services
import re
class Att_Ass_cli:
    @staticmethod
    def show_menu():
        print("\n===== ��������ҵ����ҳ�� =====")
        print("1. ���ڼ�¼")
        print("2. ��ҵ����")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def Attendance_add():#���ڼ�¼
        while True:
            StudentID = input("������ѧ��ID��").strip()
            CourseID = input("������γ�ID��").strip()
            Status=input("����������Ŀ���״̬:").strip()
            success,message=Att_Ass_Services.Attendance_add(StudentID,CourseID,Status)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def Assignment_add():#��ҵ����
        while True:
            CourseID=input("���������ҵ�����γ�ID")
            Title=input("��������ҵ����")
            Deadline=input("�������ύ��ֹʱ��(��ʽ:2025-12-31 23:34):").strip()
            success,message=Att_Ass_Services.Assignment_add(CourseID,Title,Deadline)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def run():
        Att_Ass_cli.show_menu()
        choice=1
        while True:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Att_Ass_cli.Attendance_add()
                case 2:
                    Att_Ass_cli.Assignment_add()
