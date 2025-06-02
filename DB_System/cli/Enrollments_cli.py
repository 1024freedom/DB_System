from services.Enrollments_Services import Enrollments_Servises
class Enrollments_cli:
    @staticmethod
    def show_menu():
        print("\n===== ѡ��ҳ�� =====")
        print("1. ��ѡ�γ̲�ѯ")
        print("2. ѧ���˿�")
        print("3. ѧ��ѡ�μ�¼��ѯ")
        print("4. ѧ��ѡ��")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def enroll_avail_ask():#��ѡ�γ̲�ѯ
        current_page=1
        while True:
            success,results=Enrollments_Servises.students_enroll_avail(current_page)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print("��ѡ�γ�:")
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(
                      "�γ�ID", "�γ�����","ѧ��", "�ڿν�ʦ", "����", "�Ͽ�ʱ��", "�¿�ʱ��", "����"))
                print("-"*102)
                for item in result:
                     print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(
                         item['CourseID'],
                         item['CourseName'],
                         item['Credit'],
                         item['Name'],
                         item['Day'],
                         item['StartTime'],
                         item['EndTime'],
                         item['remain']
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
    def students_drop_course():#ѧ���˿�
        while True:
            while True:
                StudentID=input("������ѧ��").strip()
                if StudentID:
                    break
                else:
                    print("ѧ�Ų���Ϊ�գ�����������")
            while True:
                CourseID=input("������Ҫ��ѡ�Ŀγ�ID").strip()
                if CourseID:
                    break
                else:
                    print("�γ̺Ų���Ϊ�գ�����������")
            success,message=Enrollments_Servises.students_drop_course(StudentID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def student_enroll_ask():#ѧ��ѡ�μ�¼��ѯ
        while True:
            StudentID=input("������ѧ��").strip()
            if StudentID:
                break
            else:
                print("ѧ�Ų���Ϊ�գ�����������")
        current_page=1
        while True:
            success,results=Enrollments_Servises.students_enroll_ask(current_page,StudentID)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                        "ѡ�μ�¼ID","ѧ��ID","ѧ������","�γ�ID","�γ���","�ڿν�ʦ","����","�Ͽ�ʱ��","�¿�ʱ��"))
                print("-"*95)
                for item in result:
                        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                            item['EnrollmentID'],
                            item['StudentID'],
                            item['StudentName'],
                            item['CourseID'],
                            item['CourseName'],
                            item['TeacherName'],
                            item['Day'],
                            item['StartTime'],
                            item['EndTime']
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
    def students_enroll():#ѧ��ѡ��
        #ѡ��γ�
        while True:
            while True:
                StudentID=input("������ѧ��").strip()
            if StudentID:
                break
            else:
                print("ѧ�Ų���Ϊ�գ�����������")
            while True:
                CourseID=input("������Ҫѡ��Ŀγ�ID(����q�˳�)").strip()
                if CourseID.lower()=='q':
                    return
                elif not CourseID:
                    print("�γ�ID����Ϊ�գ�����������")
            success,message=Enrollments_Servises.students_enroll(StudentID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def run():
        Enrollments_cli.show_menu()
        choice=1
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Enrollments_cli.enroll_avail_ask()
                case 2:
                    Enrollments_cli.students_drop_course()
                case 3:
                    Enrollments_cli.student_enroll_ask()
                case 4:
                    Enrollments_cli.students_enroll()