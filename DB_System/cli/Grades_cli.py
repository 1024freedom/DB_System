import stat
from services.Grades_Services import Grades_Services
class Grades_cli:
    @staticmethod
    def show_menu():
        print("\n===== 成绩管理页面 =====")
        print("1. 单条成绩录入")
        print("2. 成绩警告名单")
        print("0. 退出")
        print("========================")
    @staticmethod
    def grades_insert_once():#单条成绩录入
        while True:
            while True:
                StudentID = input("请输入学生ID：").strip()
                if not StudentID:
                    print("学生ID不能为空，请重新输入：")
                else:
                    break
            while True:
                CourseID = input("请输入课程ID：").strip()
                if not CourseID:
                    print("课程ID不能为空，请重新输入：")
                else:
                    break
            while True:
                Score=input("请输入要录取的成绩分数(0~100):")
                if Score>100 or Score<0:
                    print("输入的成绩不合法,请重新输入")
                else:
                    break
            success,message=Grades_Services.grades_insert_once(StudentID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def grades_alert_ask():#成绩警告名单查询
        current_page=1
        while True:
            success,results=Grades_Services.grades_alert(current_page)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                        "警告学生ID","课程ID","学生姓名","课程名","分数"))
                print("-"*50)
                for item in result:
                        print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                            item['StudentID'],
                            item['CourseID'],
                            item['StudentName'],
                            item['CourseName'],
                            item['Score']
                            ))
                    #分页导航
                if total_pages>1:
                        action=input("请输入操作:n:下一页 p:下一页 j:跳转目标页 q:退出 ").lower()
                        if action=='n':
                            current_page=min(current_page+1,total_pages)
                        elif action=='p':
                            current_page=max(current_page-1,1)
                        elif action=='j':
                            target=int(input(f"请输入目标页(1-{total_pages})"))
                            current_page=max(1,min(target,total_pages))
                        elif action=='q':
                            break
                        else:
                            print("无效操作码")
                else:
                        input("没有更多页,按任意键返回")
                        break
            else:
                print('\033[91m' + results + '\033[0m')#红色文本
    @staticmethod
    def run():
        Grades_cli.show_menu()
        choice=1
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Grades_cli.grades_insert_once()
                case 2:
                    Grades_cli.grades_alert_ask()
                