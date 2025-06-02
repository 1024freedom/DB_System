from numpy import True_
from services.Reservations_Services import Reservation_Services
class Reservation_cli:
    @staticmethod
    def show_menu():
        print("\n===== ԤԼ����ҳ�� =====")
        print("1. ʵ����ԤԼ")
        print("2. ԤԼ��¼��ѯ")
        print("3. ȡ��δ��ʼ��ԤԼ")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def lab_reservation():#ʵ����ԤԼ
        while True:
            while True:
                TeacherID=input("���������Ľ�ʦID")
                if TeacherID:
                    break
                else:
                    print("��ʦID����Ϊ��,����������")
            while True:
                LabID=input("������ҪԤԼ��ʵ����ID")
                if LabID:
                    break
                else:
                    print("ʵ����ID����Ϊ��,����������")
            while True:
                StartTime=input("�����뿪ʼʹ��ʱ��(ʾ��):2025-12-31 23:34):").strip()
                if not StartTime:
                    print("��ʼʱ�䲻��Ϊ��")
                    continue
                EndTime=input("���������ʹ��ʱ��(ʾ��):2025-12-31 23:34):").strip()
                if not EndTime:
                    print("����ʱ�䲻��Ϊ��")
                else:
                    break
            success,message=Reservation_Services.lab_reservation(TeacherID,LabID,StartTime,EndTime)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def reservation_ask():#ԤԼ��¼��ѯ
        while True:
            TeacherID=input("���������Ľ�ʦID")
            if TeacherID:
                break
            else:
                print("��ʦID����Ϊ��,����������")
        current_page=1
        while True:
            success,results=Reservation_Services.reservation_ask(current_page,TeacherID)
            if success:
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
            else:
                print('\033[91m' + results + '\033[0m')#��ɫ�ı�
    @staticmethod
    def reservation_cancel():#ȡ��δ��ʼ��ԤԼ
        while True:
            while True:
                    TeacherID=input("���������Ľ�ʦID")
                    if TeacherID:
                        break
                    else:
                        print("��ʦID����Ϊ��,����������")
            while True:
                ReservationID=input("������Ҫȡ����ԤԼ��¼ID")
                if ReservationID:
                    break
                else:
                    print("ԤԼ��¼ID����Ϊ��,����������")
            success,message=Reservation_Services.reservation_cancel(TeacherID,ReservationID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def run():
        Reservation_cli.show_menu()
        choice=1
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Reservation_cli.lab_reservation()
                case 2:
                    Reservation_cli.reservation_ask()
                case 3:
                    Reservation_cli.reservation_cancel()
                