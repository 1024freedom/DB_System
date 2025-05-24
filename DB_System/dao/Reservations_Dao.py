from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
from datetime import datetime
class Reservations_Dao:
    def lab_reservation():#实验室预约
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        while True:
            TeacherID=input("请输入您的教师ID")
            if TeacherID:
                cursor.execute("SELECT 1 FROM Teachers WHERE TeacherID=%s"(TeacherID))
                if not cursor.fetchone():
                    print("该教师ID不存在,请重新输入")
                else:
                    break
            else:
                print("教师ID不能为空,请重新输入")
        while True:
            LabID=input("请输入要预约的实验室ID")
            if LabID:
                cursor.execute("SELECT 1 FROM Classrooms WHERE ClassroomID=%s",(LabID,))
                if cursor.fetchone():
                    cursor.execute("SELECT Type FROM Cassrooms WHERE ClassroomID=%s"(LabID))
                    Type=cursor.fetchone()
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
        #校验时间冲突 
            cursor.execute("""SELECT 
                                l.StartTime,
                                l.EndTime 
                                FROM Labreservations l
                                WHERE l.LabID=%s
                            """,(LabID,))
            exist=False
            for(exist_start,exist_end) in cursor.fetchall():
                    
                    if (StartTime>exist_start and StartTime<exist_end) or (EndTime>exist_start and EndTime<exist_end):
                        print(f"该时间段{StartTime}-{EndTime}已被预约，请重新选择")
                        exist=True
                        break
            if not exist:
                break
        try:
            cursor.execute("INSERT INTO Labreserations (TeacherID,LabID,StartTime,EndTime) VALUES (%s,%s,%s,%s)",(TeacherID,LabID,StartTime,EndTime))
            conn.commit()
            print(f"实验室(ID:{LabID})预约成功")
        except Exception as e:
            conn.rollback()
            print(f"预约失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def reservation_ask():#预约记录查询
        try:
            conn = DBPool.get_instance().get_conn()
            cursor = conn.cursor()
            while True:
                TeacherID=input("请输入您的教师ID")
                if TeacherID:
                    cursor.execute("SELECT 1 FROM Teachers WHERE TeacherID=%s"(TeacherID))
                    if not cursor.fetchone():
                        print("该教师ID不存在,请重新输入")
                    else:
                        break
                else:
                    print("教师ID不能为空,请重新输入")
            #预约记录视图
                    """CREATE VIEW Lab_Reservations AS
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
        #获取总记录数
            cursor.execute("SELECT COUNT(*) AS total FROM Lab_Reservations ")
            total_records=cursor.fetchone()['total']
            if total_records==0:
                print("当前没有数据")
                return
            #设置分页参数
            page_size=20#默认每页显示20条
            total_pages=(total_records+page_size-1)//page_size#向上取整
            current_page=1
            while True:
                #计算偏移量
                offset=(current_page-1)*page_size
                #分页查询
                cursor.execute("""SELECT
                                ReservationID,
                                TeacherID,
                                TeacherName,
                                LabID,
                                StartTime,
                                EndTime
                                FROM Lab_Reservations
                                LIMIT %s OFFSET %s
                                """(page_size,offset))


                reservations=cursor.fetchall()
                if not reservations:
                    print("无预约记录")
                    return
                #显示数据准备
                display_data=[]
               
                for reservation in reservations:
                    
                        display_data.append({
                            'ReservationID':reservation['ReservationID'],
                            'TeacherID':reservation['TeacherID'],
                            'TeacherName':reservation['TeacherName'],
                            'LabID':reservation['LabID'],
                            'StartTime':reservation['StartTime'],
                            'EndTime':reservation['EndTime'],
                            'Location':reservation['Location']
                            })
                    #打印
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                        "预约记录ID","教师ID","教师姓名","实验室ID","开始使用时间","结束使用时间"))
                print("-"*70)
                for item in display_data:
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
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"操作失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def reservation_cancel():#取消未开始的预约
            conn = DBPool.get_instance().get_conn()
            cursor = conn.cursor()
            while True:
                TeacherID=input("请输入您的教师ID")
                if TeacherID:
                    cursor.execute("SELECT 1 FROM Lab_Reservations WHERE TeacherID=%s",(TeacherID,))
                    if not cursor.fetchone():
                        print("该教师ID无预约记录或该教师ID不存在,请重新输入")
                    else:
                        break
                else:
                    print("教师ID不能为空,请重新输入")
            #获取当前时间
            DateTime=datetime.today()
            try:
                while True:
                    ReservationID=input("请输入要取消的预约记录ID")
                    if ReservationID:
                        cursor.execute("SELECT 1 FROM LabReservations WHERE ReservationID=%s",(ReservationID))
                        if not cursor.fetchone():
                            print("该预约记录不存在,请重新输入")
                        else:
                            break
                    else:
                        print("预约记录ID不能为空,请重新输入")
                    cursor.execute("SELECT StartTime FROM LabReservations WHERE ReservationID=%s",(ReservationID))
                    re_datetime=cursor.fetchone()
                    if DateTime<re_datetime[0]:
                        cursor.execute("DELETE FROM LabReservations WHERE TeacherID=%s AND ReservationID=%s",(TeacherID,ReservationID,))
                        conn.commit()
                        print("取消成功")
                    else:
                        print("时间不合法")
            except Exception as e:
                conn.rollback()
                print(f"操作失败：{str(e)}")
            finally:
                cursor.close()
                conn.close()