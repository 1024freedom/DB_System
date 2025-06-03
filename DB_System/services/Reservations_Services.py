from dao.Reservations_Dao import Reservations_Dao
from dao.Askpages_Dao import Askpages_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import datetime
import re
class Reservation_Services:
    @staticmethod
    def lab_reservation(TeacherID,LabID,StartTime,EndTime):#实验室预约
        try:
            if not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                return False,"该教师ID不存在,请重新输入"
            if Search_Dao.search1('Classrooms','ClassroomID',LabID):
                Type=Fetch_Dao.fetch('Type','Classrooms','ClassroomID',LabID)
                if Type[0]!="实验室":
                    return False,"该房间不是实验室,请重新输入"
            else:
                return False,"该房间不存在,请重新输入"
            pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#时间格式
            if not re.match(pattern,StartTime):
                return False,"格式错误,请使用示例格式"
            if not re.match(pattern,EndTime):
                return False,"格式错误,请使用示例格式"
            sql="""SELECT 
                    l.StartTime,
                    l.EndTime 
                    FROM Labreservations l
                    WHERE l.LabID=%s
                """
            params=(LabID)
            for(exist_start,exist_end) in Fetch_Dao.fetchof(sql,params):    
                if (StartTime>exist_start and StartTime<exist_end) or (EndTime>exist_start and EndTime<exist_end):
                    return False,f"该时间段{StartTime}-{EndTime}已被预约，请重新选择"
            Reservations_Dao.lab_reservation(TeacherID,LabID,StartTime,EndTime)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
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
            if not Search_Dao.search1('vw_Lab_Reservations','TeacherID',ID):
                return False,"该教师ID无预约记录或该教师ID不存在,请重新输入"
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page,ID)
            #显示数据准备
               
            #(显示逻辑处理)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def reservation_cancel(TeacherID,ReservationID):#取消未开始的预约
            if not Search_Dao.search1('vw_Lab_Reservations','TeacherID',TeacherID):
                return False,"该教师ID无预约记录或该教师ID不存在,请重新输入"
            #获取当前时间
            DateTime=datetime.today()
            if not Search_Dao.search1('LabReservations','ReservationID',ReservationID):
                return False,"该预约记录不存在,请重新输入"
                
            re_datetime=Fetch_Dao.fetch('StartTime','LabReservations','ReservationID',ReservationID)
            if DateTime<re_datetime[0]:
                try:
                    Reservations_Dao.reservation_cancel(TeacherID,ReservationID)
                    return True,"操作成功"
                except Exception as e:
                    return False,f"{str(e)}"
            else:
                return False,"时间不合法"