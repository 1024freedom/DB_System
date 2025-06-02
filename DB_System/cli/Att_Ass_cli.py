from services.Att_Ass_Services import Att_Ass_Services
import re
class Att_Ass_cli:
    @staticmethod
    def show_menu():
        print("\n===== 考勤与作业管理页面 =====")
        print("1. 考勤记录")
        print("2. 作业发布")
        print("0. 退出")
        print("========================")
    @staticmethod
    def Attendance_add():#考勤记录
        while True:
            StudentID = input("请输入学生ID：").strip()
            CourseID = input("请输入课程ID：").strip()
            Status=input("请输入该生的考勤状态:").strip()
            success,message=Att_Ass_Services.Attendance_add(StudentID,CourseID,Status)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def Assignment_add():#作业发布
        while True:
            CourseID=input("请输入该作业关联课程ID")
            Title=input("请输入作业标题")
            Deadline=input("请输入提交截止时间(格式:2025-12-31 23:34):").strip()
            success,message=Att_Ass_Services.Assignment_add(CourseID,Title,Deadline)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def run():
        Att_Ass_cli.show_menu()
        choice=1
        while True:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Att_Ass_cli.Attendance_add()
                case 2:
                    Att_Ass_cli.Assignment_add()
