from services.Students_Services import Students_Services
class Students_cli:
    @staticmethod
    def show_menu():
        print("\n===== ѧ����Ϣ����ҳ�� =====")
        print("1. ��������ѧ����Ϣ")
        print("2. ����ѧ����ϵ��ʽ")
        print("3. Ϊѧ������༶")
        print("4. ɾ��ѧ����Ϣ")
        print("5. ��excel�ļ�����ѧ����Ϣ")
        print("6. ����ѧ����ϢΪexcel�ļ�")
        print("0. �˳�")
        print("========================")
    @staticmethod
    def add_student_once():#��������ѧ����Ϣ
        while True:
            while True:
                Name=input('����������').strip()
                if Name:
                    break
                print("��������Ϊ�գ�����������")
            while True:
                Gender=input('�����Ա���/Ů����').strip()
                if Gender in ('��','Ů'):
                    break
                print ("��������ȷ���Ա�")
            while True:
                BirthDate=input('��������ȷ�ĳ��������գ���ʽ��YYYY-MM-DD').strip()
                if BirthDate:
                    break
                else:
                    print("����Ϊ�գ�����������")
            while True:
                Phone=input("�������ֻ��ţ�").strip()
                if not Phone:
                    Phone=None
                    break
                if len(Phone)!=11:
                    print("�������ֻ��ų��Ȳ��Ϸ�������������")
                else:
                    break
            success,message=Students_Services.add_student_once(Name,Gender,BirthDate,Phone)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def alter_student_phone():#����ѧ����ϵ��ʽ
        while True:
            while True:
                StudentID=input("������ѧ��ID��").strip()
                if not StudentID:
                    print("ѧ��ID����Ϊ�գ�����������")
                else:
                    break
            while True:
                Phone=input("�������ֻ��ţ�").strip()
                if len(Phone)!=11:
                    print("�������ֻ��Ų��Ϸ�������������")
                else:
                    break
            success,message=Students_Services.alter_student_phone(StudentID,Phone)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def alter_student_class():#Ϊѧ������༶
        while True:
            while True:
                StudentID=input("������ѧ��ID��").strip()
                if not StudentID:
                    print("ѧ��ID����Ϊ�գ�����������")
                else:
                    break
            while True:
                ClassID=input("������ҪΪ��ѧ������İ༶�ţ�")
                if not ClassID:
                    print("�༶�Ų���Ϊ�գ�����������")
                else:
                    break
            success,message=Students_Services.alter_student_class(StudentID,ClassID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def delete_student():  # ɾ��ѧ����Ϣ
        while True:
            while True:
                StudentID = input("������ѧ��ID��").strip()
                if not StudentID:
                    print("ѧ��ID����Ϊ�գ�����������")
                else:
                    break
            success,message=Students_Services.delete_student(StudentID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def import_from_excel():#��excel�ļ�����ѧ�����ݵ����ݿ�
        filepath=input("�������ļ��ľ���·��")
        success,message=Students_Services.import_from_excel(filepath)
        if success:
            print(message)
        else:
            print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def export_to_excel():#��excel�ļ���ʽ��������ѧ����Ϣ
        filepath=input("�����뵼��·��")
        success,message=Students_Services.export_to_excel(filepath)
        if success:
            print(message)
        else:
            print('\033[91m' + message + '\033[0m')#��ɫ�ı�
    @staticmethod
    def run():
        Students_cli.show_menu()
        choice=1
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Students_cli.add_student_once()
                case 2:
                    Students_cli.alter_student_phone()
                case 3:
                    Students_cli.alter_student_class()
                case 4:
                    Students_cli.delete_student()
                case 5:
                    Students_cli.import_from_excel()
                case 6:
                    Students_cli.export_to_excel()
               