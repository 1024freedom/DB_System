from cli.Att_Ass_cli import Att_Ass_cli
from cli.Courses_cli import Courses_cli
from cli.Enrollments_cli import Enrollments_cli
from cli.Grades_cli import Grades_cli
from cli.Loans_cli import Loans_cli
from cli.main_menu import main_menu
from cli.Register_cli import Register_cli
from cli.Reservations_cli import Reservation_cli
from cli.Students_cli import Students_cli
from cli.Userlogin_cli import Userlogin_cli
def main():
    main_menu.main_menu_show()
    """print("===== �������ϵͳ =====")
        print("1. �û�ע��")
        print("2. �û���¼")
        print("3. �˳�ϵͳ")
        print("���������ѡ��")
        print("========================")"""
    choice=1
    while choice:#ע����¼��ֱ�ӵ�¼
        choice=input("��ѡ�������").strip()
        match choice:
            case 1:
                Register_cli.run()
            case 2:
                Userlogin_cli.run()
            case 3:
                break
    """# ѧ���˵�
        if role == 'ѧ��':
            print("1. ѡ��ģ��")
            print("2. ����ģ��")
            print("3. ԤԼģ��")
            print("4. �޸ĸ�����Ϣ")
        
        # ��ʦ�˵�
        elif role == '��ʦ':
            print("1. ��������ҵ����ģ��")
            print("2. �γ̹���ģ��")
            print("3. �ɼ�����ģ��")
            print("4. ����ģ��")
            print("5. ѧ����Ϣ����ģ��")
        
        # ����Ա�˵�
        elif role == '����Ա':
            print("1. �û�����")
            print("2. Ȩ�޹���")
            print("3. ϵͳ����")"""
            #��½��
    if Userlogin_cli.current_role=='ѧ��':
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Enrollments_cli.run()
                case 2:
                    Loans_cli.run()
                case 3:
                    Reservation_cli.run()
                case 4:
                    Students_cli.run()
    if Userlogin_cli.current_role=='��ʦ':
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Att_Ass_cli.run()
                case 2:
                    Courses_cli.run()
                case 3:
                    Grades_cli.run()
                case 4:
                    Loans_cli.run()
                case 5:
                    Students_cli.run()
    """if Userlogin_cli.current_role=='����Ա':
        while choice:
            choice=input("��ѡ�������").strip()
            match choice:
                case 1:
                    Register_cli.run()
                case 2:
                    Userlogin_cli.run()
                case 3:
                    break"""
if __name__ == "__main__":
    main()




