from services.Reservations_Services import Reservation_Services
from services.Grades_Services import Grades_Services
from services.Enrollments_Services import Enrollments_Servises
from services.Courses_Services import Course_Services
from dao.Search_Dao import Search_Dao
def reservation_ask():#ԤԼ��¼��ѯ
    while True:
        TeacherID=input("���������Ľ�ʦID")
        if TeacherID:
            if not Search_Dao.search1('vw_Lab_Reservations','TeacherID',TeacherID):
                print("�ý�ʦID��ԤԼ��¼��ý�ʦID������,����������")
            else:
                break
        else:
            print("��ʦID����Ϊ��,����������")
    current_page=1
    while True:
        results=Reservation_Services.reservation_ask(current_page,TeacherID)
        result=results['data']
        total_pages=results['total_pages']
        print(f"��ǰҳ��:{current_page}/{total_pages}")
        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                "ԤԼ��¼ID","��ʦID","��ʦ����","ʵ����ID","��ʼʹ��ʱ��","����ʹ��ʱ��"))
        print("-"*70)
        for item in result:
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                    item['ReservationID'],
                    item['TeacherID'],
                    item['TeacherName'],
                    item['LabID'],
                    item['StartTime'],
                    item['EndTime'],
                    item['Location']
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
def grades_alert_ask():#�ɼ�����������ѯ
    current_page=1
    while True:
        results=Grades_Services.grades_alert(current_page)
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
def student_enroll_ask():#ѧ��ѡ�μ�¼��ѯ
    while True:
        StudentID=input("������ѧ��").strip()
        if StudentID:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("ѧ�Ų����ڣ�����������")
            else:
                break
        else:
            print("ѧ�Ų���Ϊ�գ�����������")
    current_page=1
    while True:
        results=Enrollments_Servises.students_enroll_ask(current_page,StudentID)
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
def enroll_avail_ask():#��ѡ�γ̲�ѯ
    current_page=1
    while True:
        results=Enrollments_Servises.students_enroll_avail(current_page)
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
def course_capacity_show():#�γ���������
    current_page=1
    while True:
        results=Course_Services.course_capacity(current_page)
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


