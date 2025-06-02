import stat
from services.Grades_Services import Grades_Services
class Grades_cli:
    @staticmethod
    def show_menu():
        print("\n===== �ɼ�����ҳ�� =====")
        print("1. �����ɼ�¼��")
        print("2. �ɼ���������")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def grades_insert_once():#�����ɼ�¼��
        while True:
            while True:
                StudentID = input("������ѧ��ID��").strip()
                if not StudentID:
                    print("ѧ��ID����Ϊ�գ����������룺")
                else:
                    break
            while True:
                CourseID = input("������γ�ID��").strip()
                if not CourseID:
                    print("�γ�ID����Ϊ�գ����������룺")
                else:
                    break
            while True:
                Score=input("������Ҫ¼ȡ�ĳɼ�����(0~100):")
                if Score>100 or Score<0:
                    print("����ĳɼ����Ϸ�,����������")
                else:
                    break
            success,message=Grades_Services.grades_insert_once(StudentID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def grades_alert_ask():#�ɼ�����������ѯ
        current_page=1
        while True:
            success,results=Grades_Services.grades_alert(current_page)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                        "����ѧ��ID","�γ�ID","ѧ������","�γ���","����"))
                print("-"*50)
                for item in result:
                        print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                            item['StudentID'],
                            item['CourseID'],
                            item['StudentName'],
                            item['CourseName'],
                            item['Score']
                            ))
                    #��ҳ����
                if total_pages>1:
                        action=input("���������:n:��һҳ p:��һҳ j:��תĿ��ҳ q:�˳� ").lower()
                        if action=='n':
                            current_page=min(current_page+1,total_pages)
                        elif action=='p':
                            current_page=max(current_page-1,1)
                        elif action=='j':
                            target=int(input(f"������Ŀ��ҳ(1-{total_pages})"))
                            current_page=max(1,min(target,total_pages))
                        elif action=='q':
                            break
                        else:
                            print("��Ч������")
                else:
                        input("û�и���ҳ,�����������")
                        break
            else:
                print('\033[91m' + results + '\033[0m')#��ɫ�ı�
    @staticmethod
    def run():
        Grades_cli.show_menu()
        choice=1
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Grades_cli.grades_insert_once()
                case 2:
                    Grades_cli.grades_alert_ask()
                