from services.Enrollments_Services import Enrollments_Servises
class Enrollments_cli:
    @staticmethod
    def show_menu():
        print("\n===== 选课页面 =====")
        print("1. 可选课程查询")
        print("2. 学生退课")
        print("3. 学生选课记录查询")
        print("4. 学生选课")
        print("0. 退出")
        print("========================")
    @staticmethod
    def enroll_avail_ask():#可选课程查询
        current_page=1
        while True:
            success,results=Enrollments_Servises.students_enroll_avail(current_page)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print("可选课程:")
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(
                      "课程ID", "课程名称","学分", "授课教师", "星期", "上课时间", "下课时间", "余量"))
                print("-"*102)
                for item in result:
                     print("{:<10}{:<20}{:<7}{:<15}{:<5}{:<15}{:<15}{:<15}".format(
                         item['CourseID'],
                         item['CourseName'],
                         item['Credit'],
                         item['Name'],
                         item['Day'],
                         item['StartTime'],
                         item['EndTime'],
                         item['remain']
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
    def students_drop_course():#学生退课
        while True:
            while True:
                StudentID=input("请输入学号").strip()
                if StudentID:
                    break
                else:
                    print("学号不能为空，请重新输入")
            while True:
                CourseID=input("请输入要退选的课程ID").strip()
                if CourseID:
                    break
                else:
                    print("课程号不能为空，请重新输入")
            success,message=Enrollments_Servises.students_drop_course(StudentID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def student_enroll_ask():#学生选课记录查询
        while True:
            StudentID=input("请输入学号").strip()
            if StudentID:
                break
            else:
                print("学号不能为空，请重新输入")
        current_page=1
        while True:
            success,results=Enrollments_Servises.students_enroll_ask(current_page,StudentID)
            if success:
                result=results['data']
                total_pages=results['total_pages']
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                        "选课记录ID","学生ID","学生姓名","课程ID","课程名","授课教师","星期","上课时间","下课时间"))
                print("-"*95)
                for item in result:
                        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                            item['EnrollmentID'],
                            item['StudentID'],
                            item['StudentName'],
                            item['CourseID'],
                            item['CourseName'],
                            item['TeacherName'],
                            item['Day'],
                            item['StartTime'],
                            item['EndTime']
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
    def students_enroll():#学生选课
        #选择课程
        while True:
            while True:
                StudentID=input("请输入学号").strip()
            if StudentID:
                break
            else:
                print("学号不能为空，请重新输入")
            while True:
                CourseID=input("请输入要选择的课程ID(输入q退出)").strip()
                if CourseID.lower()=='q':
                    return
                elif not CourseID:
                    print("课程ID不能为空，请重新输入")
            success,message=Enrollments_Servises.students_enroll(StudentID,CourseID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def run():
        Enrollments_cli.show_menu()
        choice=1
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Enrollments_cli.enroll_avail_ask()
                case 2:
                    Enrollments_cli.students_drop_course()
                case 3:
                    Enrollments_cli.student_enroll_ask()
                case 4:
                    Enrollments_cli.students_enroll()