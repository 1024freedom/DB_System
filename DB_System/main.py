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
    """print("===== 教务管理系统 =====")
        print("1. 用户注册")
        print("2. 用户登录")
        print("3. 退出系统")
        print("请输入你的选择：")
        print("========================")"""
    choice=1
    while choice:#注册后登录或直接登录
        choice=input("请选择操作：").strip()
        match choice:
            case 1:
                Register_cli.run()
            case 2:
                Userlogin_cli.run()
            case 3:
                break
    """# 学生菜单
        if role == '学生':
            print("1. 选课模块")
            print("2. 借用模块")
            print("3. 预约模块")
            print("4. 修改个人信息")
        
        # 教师菜单
        elif role == '教师':
            print("1. 考勤与作业管理模块")
            print("2. 课程管理模块")
            print("3. 成绩管理模块")
            print("4. 借用模块")
            print("5. 学生信息管理模块")
        
        # 管理员菜单
        elif role == '管理员':
            print("1. 用户管理")
            print("2. 权限管理")
            print("3. 系统设置")"""
            #登陆后
    if Userlogin_cli.current_role=='学生':
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Enrollments_cli.run()
                case 2:
                    Loans_cli.run()
                case 3:
                    Reservation_cli.run()
                case 4:
                    Students_cli.run()
    if Userlogin_cli.current_role=='教师':
        while choice:
            choice=input("请选择操作：").strip()
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
    """if Userlogin_cli.current_role=='管理员':
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Register_cli.run()
                case 2:
                    Userlogin_cli.run()
                case 3:
                    break"""
if __name__ == "__main__":
    main()




