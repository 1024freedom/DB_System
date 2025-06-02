from services.Register_Services import Register_Services
class Register_cli:
    @staticmethod
    def show_menu():#���˵�
        print("\n===== �û�ע��ҳ�� =====")
        print("1. ѧ��ע��")
        print("2. ��ʦע��")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def register_student():#ע��ѧ���û�
        print("\n===== ѧ��ע�� =====")
        while True:
            user_id=input("������ѧ��id").strip()
            password=input("���������루��������Ϊ��λ��������Сд��ĸ������").strip()
            confirm_password=input("���ٴ���������ȷ��").strip()
            if password!=confirm_password:
                print("���벻һ�£������²���")
                continue
            success,message=Register_Services.register_student(user_id,password)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def register_teacher():#ע���ʦ�û�
        print("\n===== ��ʦע�� =====")
        while True:
            user_id=input("�������ʦid").strip()
            password=input("���������루��������Ϊ��λ��������Сд��ĸ������").strip()
            confirm_password=input("���ٴ���������ȷ��").strip()
            if password!=confirm_password:
                print("���벻һ�£������²���")
                continue
            success,message=Register_Services.register_teacher(user_id,password)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def run():
        Register_cli.show_menu()
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Register_cli.register_student()
                case 2:
                    Register_cli.register_teacher()
                


