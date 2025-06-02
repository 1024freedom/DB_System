from numpy import True_
from services.Courses_Services import Course_Services
class Courses_cli:
    @staticmethod
    def show_menu():
        print("\n===== 课程管理页面 =====")
        print("1. 新增课程")
        print("2. 编辑课程名称")
        print("3. 编辑课程学分")
        print("4. 编辑授课教师")
        print("5. 为课程绑定教材")
        print("6. 课程容量监视")
        print("7. 排课")
        print("0. 退出")
        print("========================")
    @staticmethod
    def add_courses():#新增课程
        while True:
            while True:
                CourseName=input("请输入课程名称").strip()
                if CourseName:
                    break
                print("课程名不能为空，请重新输入")
            while True:
                Credit=input("请输入该课程的学分").strip()
                if Credit:
                    break
                print("不能为空，请重新输入")
            TeacherID=input("请输入教师ID")
            success,message=Course_Services.add_courses(CourseName,Credit,TeacherID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def edit_courses_name():#编辑课程名称
        while True:
            while True:
                CourseID=input("请输入要操作的课程ID").strip()
                if not CourseID:
                    print("课程ID不能为空，请重新输入")
                else:
                    break
            while True:
                newCourseName=input("请输入新名称").strip()
                if newCourseName:
                    break
                else:
                    print("课程名不能为空，请重新输入")
            success,message=Course_Services.edit_courses_name(CourseID,newCourseName)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def edit_courses_credit():#编辑课程学分
        while True:
            while True:
                CourseID=input("请输入要操作的课程ID").strip()
                if not CourseID:
                    print("课程ID不能为空，请重新输入")
                else:
                    break
            while True:
                newCredit=input("请输入学分").strip()
                if newCredit:
                    break
                else:
                    print("课程名不能为空，请重新输入")
            success,message=Course_Services.edit_courses_credit(CourseID,newCredit)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def edit_teachers():#编辑授课教师
        while True:
            while True:
                CourseID=input("请输入要操作的课程ID").strip()
                if not CourseID:
                    print("课程ID不能为空，请重新输入")
                else:
                    break
            while True:
                newTeacherID=input("请输入教师ID").strip()
                if newTeacherID:
                    break
                else:
                    print("ID不能为空，请重新输入")
            success,message=Course_Services.edit_teachers(CourseID,newTeacherID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def attach_course_tb():#为课程绑定教材
        while True:
            while True:
                TextbookID=input("请输入要操作的教材ID").strip()
                if not TextbookID:
                    print("教材ID不能为空，请重新输入")
                else:
                    break
            while True:
                CourseID=input("请输入要绑定的课程ID").strip()
                if not CourseID:
                    print("课程ID不能为空，请重新输入")
                else:
                    break
            success,message=Course_Services.attach_course_tb(TextbookID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def course_capacity_show():#课程容量监视
        current_page=1
        while True:
            success,results=Course_Services.course_capacity(current_page)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                        "课程ID","课程名称","容量","余量","状态"))
                print("-"*60)
                for item in result:
                        print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                            item['CourseID'],
                            item['CourseName'],
                            item['Capacity'],
                            item['remain'],
                            item['status']
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
    def course_time_arr():#排课
        while True:
            while True:
                CourseID=input("请输入要操作的课程ID")
                if CourseID:
                    break
                else:
                    print("课程ID不能为空，请重新输入")
            while True:
                Day=input("请输入上课的星期（1-7）")
                if Day:
                    if 1<=Day<=7:
                        break
                    else:
                        print("请输入数字1-7")
                else:
                    print("星期不能为空，请重新输入")
            while True:
                StartTime=input("请输入上课时间")
                EndTime=input("请输入下课时间")
                if StartTime and EndTime:
                    break
                else:
                    print("输入不能为空，请重新输入")
            success,message=Course_Services.course_time_arr(CourseID,Day,StartTime,EndTime)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本\
    @staticmethod
    def run():
        Courses_cli.show_menu()
        choice=1
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Courses_cli.add_courses()
                case 2:
                    Courses_cli.edit_courses_name()
                case 3:
                    Courses_cli.edit_courses_credit()
                case 4:
                    Courses_cli.edit_teachers()
                case 5:
                    Courses_cli.attach_course_tb()
                case 6:
                    Courses_cli.course_capacity_show()
                case 7:
                    Courses_cli.course_time_arr()