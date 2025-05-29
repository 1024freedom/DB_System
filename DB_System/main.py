from services.Reservations_Services import Reservation_Services
from services.Grades_Services import Grades_Services
from services.Enrollments_Services import Enrollments_Servises
from services.Courses_Services import Course_Services
from dao.Search_Dao import Search_Dao
def reservation_ask():#预约记录查询
    while True:
        TeacherID=input("请输入您的教师ID")
        if TeacherID:
            if not Search_Dao.search1('vw_Lab_Reservations','TeacherID',TeacherID):
                print("该教师ID无预约记录或该教师ID不存在,请重新输入")
            else:
                break
        else:
            print("教师ID不能为空,请重新输入")
    current_page=1
    while True:
        results=Reservation_Services.reservation_ask(current_page,TeacherID)
        result=results['data']
        total_pages=results['total_pages']
        print(f"当前页码:{current_page}/{total_pages}")
        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                "预约记录ID","教师ID","教师姓名","实验室ID","开始使用时间","结束使用时间"))
        print("-"*70)
        for item in result:
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                    item['ReservationID'],
                    item['TeacherID'],
                    item['TeacherName'],
                    item['LabID'],
                    item['StartTime'],
                    item['EndTime'],
                    item['Location']
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
def grades_alert_ask():#成绩警告名单查询
    current_page=1
    while True:
        results=Grades_Services.grades_alert(current_page)
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
def student_enroll_ask():#学生选课记录查询
    while True:
        StudentID=input("请输入学号").strip()
        if StudentID:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("学号不存在，请重新输入")
            else:
                break
        else:
            print("学号不能为空，请重新输入")
    current_page=1
    while True:
        results=Enrollments_Servises.students_enroll_ask(current_page,StudentID)
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
def enroll_avail_ask():#可选课程查询
    current_page=1
    while True:
        results=Enrollments_Servises.students_enroll_avail(current_page)
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
def course_capacity_show():#课程容量监视
    current_page=1
    while True:
        results=Course_Services.course_capacity(current_page)
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


