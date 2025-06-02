from sqlalchemy import true
from services.Userlogin_Services import Userlogin_Services
class Userlogin_cli:
    current_role=None#记录当前用户角色
    @staticmethod
    def show_login_menu():
        print("\n===== 用户页面 =====")
        print("1. 用户登录")
        print("2. 退出")
        print("========================")
    @staticmethod
    def login():
        while True:
            while True:
                user_id=input("请输入用户ID：").strip()
                if not user_id:
                    print("用户ID不能为空，请重新输入")
                else:
                    break
            while True:
                password=input("请输入密码：").strip()
                if not password:
                    print("密码不能为空，请重新输入")
                else:
                    break
            success,message,Userlogin_cli.current_role=Userlogin_Services.login(user_id,password)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def show_main_menu():#登录后首页
        if not Userlogin_cli.current_user:
            print("请先登录")
            return
        
        role = Userlogin_cli.current_role
        print(f"===== 主菜单 ({role} {Userlogin_cli.current_role} =====")
        
        # 学生菜单
        if role == '学生':
            print("1. 选课模块")
            print("2. 借用模块")
            print("3. 预约模块")
            print("4. 修改个人信息")
            print("0. 退出")
        
        # 教师菜单
        elif role == '教师':
            print("1. 考勤与作业管理模块")
            print("2. 课程管理模块")
            print("3. 成绩管理模块")
            print("4. 借用模块")
            print("5. 学生信息管理模块")
            print("0. 退出")
        
        # 管理员菜单
        elif role == '管理员':
            print("1. 用户管理")
            print("2. 权限管理")
            print("3. 系统设置")
            print("0. 退出")
        print("==============================")
    @staticmethod
    def run():
        Userlogin_cli.show_login_menu()
        choice=1
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Userlogin_cli.login()
                    Userlogin_cli.show_main_menu()
                case 2:
                    return 
