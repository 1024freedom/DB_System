from numpy import True_
from services.Reservations_Services import Reservation_Services
class Reservation_cli:
    @staticmethod
    def show_menu():
        print("\n===== 预约管理页面 =====")
        print("1. 实验室预约")
        print("2. 预约记录查询")
        print("3. 取消未开始的预约")
        print("0. 退出")
        print("========================")
    @staticmethod
    def lab_reservation():#实验室预约
        while True:
            while True:
                TeacherID=input("请输入您的教师ID")
                if TeacherID:
                    break
                else:
                    print("教师ID不能为空,请重新输入")
            while True:
                LabID=input("请输入要预约的实验室ID")
                if LabID:
                    break
                else:
                    print("实验室ID不能为空,请重新输入")
            while True:
                StartTime=input("请输入开始使用时间(示例):2025-12-31 23:34):").strip()
                if not StartTime:
                    print("开始时间不能为空")
                    continue
                EndTime=input("请输入结束使用时间(示例):2025-12-31 23:34):").strip()
                if not EndTime:
                    print("结束时间不能为空")
                else:
                    break
            success,message=Reservation_Services.lab_reservation(TeacherID,LabID,StartTime,EndTime)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def reservation_ask():#预约记录查询
        while True:
            TeacherID=input("请输入您的教师ID")
            if TeacherID:
                break
            else:
                print("教师ID不能为空,请重新输入")
        current_page=1
        while True:
            success,results=Reservation_Services.reservation_ask(current_page,TeacherID)
            if success:
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
            else:
                print('\033[91m' + results + '\033[0m')#红色文本
    @staticmethod
    def reservation_cancel():#取消未开始的预约
        while True:
            while True:
                    TeacherID=input("请输入您的教师ID")
                    if TeacherID:
                        break
                    else:
                        print("教师ID不能为空,请重新输入")
            while True:
                ReservationID=input("请输入要取消的预约记录ID")
                if ReservationID:
                    break
                else:
                    print("预约记录ID不能为空,请重新输入")
            success,message=Reservation_Services.reservation_cancel(TeacherID,ReservationID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def run():
        Reservation_cli.show_menu()
        choice=1
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case "1":
                    Reservation_cli.lab_reservation()
                case "2":
                    Reservation_cli.reservation_ask()
                case "3":
                    Reservation_cli.reservation_cancel()
                