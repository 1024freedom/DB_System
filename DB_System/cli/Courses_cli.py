from numpy import True_
from services.Courses_Services import Course_Services
class Courses_cli:
    @staticmethod
    def show_menu():
        print("\n===== �γ̹���ҳ�� =====")
        print("1. �����γ�")
        print("2. �༭�γ�����")
        print("3. �༭�γ�ѧ��")
        print("4. �༭�ڿν�ʦ")
        print("5. Ϊ�γ̰󶨽̲�")
        print("6. �γ���������")
        print("7. �ſ�")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def add_courses():#�����γ�
        while True:
            while True:
                CourseName=input("������γ�����").strip()
                if CourseName:
                    break
                print("�γ�������Ϊ�գ�����������")
            while True:
                Credit=input("������ÿγ̵�ѧ��").strip()
                if Credit:
                    break
                print("����Ϊ�գ�����������")
            TeacherID=input("�������ʦID")
            success,message=Course_Services.add_courses(CourseName,Credit,TeacherID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def edit_courses_name():#�༭�γ�����
        while True:
            while True:
                CourseID=input("������Ҫ�����Ŀγ�ID").strip()
                if not CourseID:
                    print("�γ�ID����Ϊ�գ�����������")
                else:
                    break
            while True:
                newCourseName=input("������������").strip()
                if newCourseName:
                    break
                else:
                    print("�γ�������Ϊ�գ�����������")
            success,message=Course_Services.edit_courses_name(CourseID,newCourseName)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def edit_courses_credit():#�༭�γ�ѧ��
        while True:
            while True:
                CourseID=input("������Ҫ�����Ŀγ�ID").strip()
                if not CourseID:
                    print("�γ�ID����Ϊ�գ�����������")
                else:
                    break
            while True:
                newCredit=input("������ѧ��").strip()
                if newCredit:
                    break
                else:
                    print("�γ�������Ϊ�գ�����������")
            success,message=Course_Services.edit_courses_credit(CourseID,newCredit)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def edit_teachers():#�༭�ڿν�ʦ
        while True:
            while True:
                CourseID=input("������Ҫ�����Ŀγ�ID").strip()
                if not CourseID:
                    print("�γ�ID����Ϊ�գ�����������")
                else:
                    break
            while True:
                newTeacherID=input("�������ʦID").strip()
                if newTeacherID:
                    break
                else:
                    print("ID����Ϊ�գ�����������")
            success,message=Course_Services.edit_teachers(CourseID,newTeacherID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def attach_course_tb():#Ϊ�γ̰󶨽̲�
        while True:
            while True:
                TextbookID=input("������Ҫ�����Ľ̲�ID").strip()
                if not TextbookID:
                    print("�̲�ID����Ϊ�գ�����������")
                else:
                    break
            while True:
                CourseID=input("������Ҫ�󶨵Ŀγ�ID").strip()
                if not CourseID:
                    print("�γ�ID����Ϊ�գ�����������")
                else:
                    break
            success,message=Course_Services.attach_course_tb(TextbookID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def course_capacity_show():#�γ���������
        current_page=1
        while True:
            success,results=Course_Services.course_capacity(current_page)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                        "�γ�ID","�γ�����","����","����","״̬"))
                print("-"*60)
                for item in result:
                        print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                            item['CourseID'],
                            item['CourseName'],
                            item['Capacity'],
                            item['remain'],
                            item['status']
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
    def course_time_arr():#�ſ�
        while True:
            while True:
                CourseID=input("������Ҫ�����Ŀγ�ID")
                if CourseID:
                    break
                else:
                    print("�γ�ID����Ϊ�գ�����������")
            while True:
                Day=input("�������Ͽε����ڣ�1-7��")
                if Day:
                    if 1<=Day<=7:
                        break
                    else:
                        print("����������1-7")
                else:
                    print("���ڲ���Ϊ�գ�����������")
            while True:
                StartTime=input("�������Ͽ�ʱ��")
                EndTime=input("�������¿�ʱ��")
                if StartTime and EndTime:
                    break
                else:
                    print("���벻��Ϊ�գ�����������")
            success,message=Course_Services.course_time_arr(CourseID,Day,StartTime,EndTime)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�\
    @staticmethod
    def run():
        Courses_cli.show_menu()
        choice=1
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Courses_cli.add_courses()
                case 2:
                    Courses_cli.edit_courses_name()
                case 3:
                    Courses_cli.edit_courses_credit()
                case 4:
                    Courses_cli.edit_teachers()
                case 5:
                    Courses_cli.attach_course_tb()
                case 6:
                    Courses_cli.course_capacity_show()
                case 7:
                    Courses_cli.course_time_arr()