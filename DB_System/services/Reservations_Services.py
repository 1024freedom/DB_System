from dao.Reservations_Dao import Reservations_Dao
from dao.Askpages_Dao import Askpages_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import datetime
import re
class Reservation_Services:
    @staticmethod
    def lab_reservation():#实验室预约
        while True:
            TeacherID=input("请输入您的教师ID")
            if TeacherID:
                if not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                    print("该教师ID不存在,请重新输入")
                else:
                    break
            else:
                print("教师ID不能为空,请重新输入")
        while True:
            LabID=input("请输入要预约的实验室ID")
            if LabID:
                if Search_Dao.search1('Classrooms','ClassroomID',LabID):
                    Type=Fetch_Dao.fetch('Type','Classrooms','ClassroomID',LabID)
                    if Type[0]!="实验室":
                        print("该房间不是实验室,请重新输入")
                    else:
                        break
                else:
                    print("该房间不存在,请重新输入")
            else:
                print("实验室ID不能为空,请重新输入")
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#时间格式
        while True:
            StartTime=input("请输入开始使用时间(示例):2025-12-31 23:34):").strip()
            if not StartTime:
                print("开始时间不能为空")
                continue
            if not re.match(pattern,StartTime):
                print("格式错误,请使用示例格式")
                continue
            EndTime=input("请输入结束使用时间(示例):2025-12-31 23:34):").strip()
            if not EndTime:
                print("结束时间不能为空")
                continue
            if not re.match(pattern,EndTime):
                print("格式错误,请使用示例格式")
                continue
            sql="""SELECT 
                    l.StartTime,
                    l.EndTime 
                    FROM Labreservations l
                    WHERE l.LabID=%s
                """
            params=(LabID)
            exist=False#检查时间冲突
            for(exist_start,exist_end) in Fetch_Dao.fetchof(sql,params):    
                if (StartTime>exist_start and StartTime<exist_end) or (EndTime>exist_start and EndTime<exist_end):
                    print(f"该时间段{StartTime}-{EndTime}已被预约，请重新选择")
                    exist=True
                    break
            if not exist:
                break
        try:
            Reservations_Dao.lab_reservation(LabID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def reservation_ask(current_page,ID):#预约记录查询
        #预约记录视图
        """CREATE VIEW vw_Lab_Reservations AS
                SELECT 
                    l.ReservationID,
                    l.TeacherID,
                    t.Name AS TeacherName,
                    l.LabID,
                    l.StartTime,
                    l.EndTime,
                    c.Location
                    FROM Labreservations l 
                    JOIN Teachers t ON l.TeacherID=t.TeacherID
                    JOIN Classrooms c ON l.LabID=c.ClassroomID
"""
        base_sql="""SELECT
                    ReservationID,
                    TeacherID,
                    TeacherName,
                    LabID,
                    StartTime,
                    EndTime
                    FROM vw_Lab_Reservations
                    WHERE TeacherID=%s
                    LIMIT %s OFFSET %s
        """
        count_sql="""SELECT COUNT(*) AS total FROM vm_Lab_Reservations"""
        #分页参数
        page_size=20
        try:
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page,ID)
            #显示数据准备
               
            #(显示逻辑处理)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def reservation_cancel():#取消未开始的预约
        while True:
                TeacherID=input("请输入您的教师ID")
                if TeacherID:
                    if not Search_Dao.search1('vw_Lab_Reservations','TeacherID',TeacherID):
                        print("该教师ID无预约记录或该教师ID不存在,请重新输入")
                    else:
                        break
                else:
                    print("教师ID不能为空,请重新输入")
            #获取当前时间
        DateTime=datetime.today()
            
        while True:
            ReservationID=input("请输入要取消的预约记录ID")
            if ReservationID:
                if not Search_Dao.search1('LabReservations','ReservationID',ReservationID):
                    print("该预约记录不存在,请重新输入")
                else:
                    break
            else:
                print("预约记录ID不能为空,请重新输入")
            re_datetime=Fetch_Dao.fetch('StartTime','LabReservations','ReservationID',ReservationID)
            if DateTime<re_datetime[0]:
                try:
                    Reservations_Dao.reservation_cancel(TeacherID,ReservationID)
                    return True,"操作成功"
                except Exception as e:
                    print(f"操作失败：{str(e)}")
            else:
                print("时间不合法")