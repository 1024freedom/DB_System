from sqlalchemy import true
from services.Userlogin_Services import Userlogin_Services
class Userlogin_cli:
    current_role=None#��¼��ǰ�û���ɫ
    @staticmethod
    def show_login_menu():
        print("\n===== �û�ҳ�� =====")
        print("1. �û���¼")
        print("2. �˳�")
        print("========================")
    @staticmethod
    def login():
        while True:
            while True:
                user_id=input("�������û�ID��").strip()
                if not user_id:
                    print("�û�ID����Ϊ�գ�����������")
                else:
                    break
            while True:
                password=input("���������룺").strip()
                if not password:
                    print("���벻��Ϊ�գ�����������")
                else:
                    break
            success,message,Userlogin_cli.current_role=Userlogin_Services.login(user_id,password)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def show_main_menu():#��¼����ҳ
        if not Userlogin_cli.current_user:
            print("���ȵ�¼")
            return
        
        role = Userlogin_cli.current_role
        print(f"===== ���˵� ({role} {Userlogin_cli.current_role} =====")
        
        # ѧ���˵�
        if role == 'ѧ��':
            print("1. ѡ��ģ��")
            print("2. ����ģ��")
            print("3. ԤԼģ��")
            print("4. �޸ĸ�����Ϣ")
            print("0. �˳�")
        
        # ��ʦ�˵�
        elif role == '��ʦ':
            print("1. ��������ҵ����ģ��")
            print("2. �γ̹���ģ��")
            print("3. �ɼ�����ģ��")
            print("4. ����ģ��")
            print("5. ѧ����Ϣ����ģ��")
            print("0. �˳�")
        
        # ����Ա�˵�
        elif role == '����Ա':
            print("1. �û�����")
            print("2. Ȩ�޹���")
            print("3. ϵͳ����")
            print("0. �˳�")
        print("==============================")
    @staticmethod
    def run():
        Userlogin_cli.show_login_menu()
        choice=1
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Userlogin_cli.login()
                    Userlogin_cli.show_main_menu()
                case 2:
                    return 
