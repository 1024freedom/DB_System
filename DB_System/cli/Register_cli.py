from services.Register_Services import Register_Services
class Register_cli:
    @staticmethod
    def show_menu():#主菜单
        print("\n===== 用户注册页面 =====")
        print("1. 学生注册")
        print("2. 教师注册")
        print("0. 退出")
        print("========================")
    @staticmethod
    def register_student():#注册学生用户
        print("\n===== 学生注册 =====")
        while True:
            user_id=input("请输入学生id").strip()
            password=input("请输入密码（长度至少为八位，包含大小写字母和数字").strip()
            confirm_password=input("请再次输入密码确认").strip()
            if password!=confirm_password:
                print("密码不一致，请重新操作")
                continue
            success,message=Register_Services.register_student(user_id,password)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def register_teacher():#注册教师用户
        print("\n===== 教师注册 =====")
        while True:
            user_id=input("请输入教师id").strip()
            password=input("请输入密码（长度至少为八位，包含大小写字母和数字").strip()
            confirm_password=input("请再次输入密码确认").strip()
            if password!=confirm_password:
                print("密码不一致，请重新操作")
                continue
            success,message=Register_Services.register_teacher(user_id,password)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def run():
        Register_cli.show_menu()
        choice=1
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case "1":
                    Register_cli.register_student()
                case "2":
                    Register_cli.register_teacher()
                


