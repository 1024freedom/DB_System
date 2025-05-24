from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
from datetime import datetime
class Reservations_Dao:
    def lab_reservation():#ʵ����ԤԼ
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        while True:
            TeacherID=input("���������Ľ�ʦID")
            if TeacherID:
                cursor.execute("SELECT 1 FROM Teachers WHERE TeacherID=%s"(TeacherID))
                if not cursor.fetchone():
                    print("�ý�ʦID������,����������")
                else:
                    break
            else:
                print("��ʦID����Ϊ��,����������")
        while True:
            LabID=input("������ҪԤԼ��ʵ����ID")
            if LabID:
                cursor.execute("SELECT 1 FROM Classrooms WHERE ClassroomID=%s",(LabID,))
                if cursor.fetchone():
                    cursor.execute("SELECT Type FROM Cassrooms WHERE ClassroomID=%s"(LabID))
                    Type=cursor.fetchone()
                    if Type[0]!="ʵ����":
                        print("�÷��䲻��ʵ����,����������")
                    else:
                        break
                else:
                    print("�÷��䲻����,����������")
            else:
                print("ʵ����ID����Ϊ��,����������")
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#ʱ���ʽ
        while True:
            StartTime=input("�����뿪ʼʹ��ʱ��(ʾ��):2025-12-31 23:34):").strip()
            if not StartTime:
                print("��ʼʱ�䲻��Ϊ��")
                continue
            if not re.match(pattern,StartTime):
                print("��ʽ����,��ʹ��ʾ����ʽ")
                continue
            EndTime=input("���������ʹ��ʱ��(ʾ��):2025-12-31 23:34):").strip()
            if not EndTime:
                print("����ʱ�䲻��Ϊ��")
                continue
            if not re.match(pattern,EndTime):
                print("��ʽ����,��ʹ��ʾ����ʽ")
                continue
        #У��ʱ���ͻ 
            cursor.execute("""SELECT 
                                l.StartTime,
                                l.EndTime 
                                FROM Labreservations l
                                WHERE l.LabID=%s
                            """,(LabID,))
            exist=False
            for(exist_start,exist_end) in cursor.fetchall():
                    
                    if (StartTime>exist_start and StartTime<exist_end) or (EndTime>exist_start and EndTime<exist_end):
                        print(f"��ʱ���{StartTime}-{EndTime}�ѱ�ԤԼ��������ѡ��")
                        exist=True
                        break
            if not exist:
                break
        try:
            cursor.execute("INSERT INTO Labreserations (TeacherID,LabID,StartTime,EndTime) VALUES (%s,%s,%s,%s)",(TeacherID,LabID,StartTime,EndTime))
            conn.commit()
            print(f"ʵ����(ID:{LabID})ԤԼ�ɹ�")
        except Exception as e:
            conn.rollback()
            print(f"ԤԼʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def reservation_ask():#ԤԼ��¼��ѯ
        try:
            conn = DBPool.get_instance().get_conn()
            cursor = conn.cursor()
            while True:
                TeacherID=input("���������Ľ�ʦID")
                if TeacherID:
                    cursor.execute("SELECT 1 FROM Teachers WHERE TeacherID=%s"(TeacherID))
                    if not cursor.fetchone():
                        print("�ý�ʦID������,����������")
                    else:
                        break
                else:
                    print("��ʦID����Ϊ��,����������")
            #ԤԼ��¼��ͼ
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
        #��ȡ�ܼ�¼��
            cursor.execute("SELECT COUNT(*) AS total FROM Lab_Reservations ")
            total_records=cursor.fetchone()['total']
            if total_records==0:
                print("��ǰû������")
                return
            #���÷�ҳ����
            page_size=20#Ĭ��ÿҳ��ʾ20��
            total_pages=(total_records+page_size-1)//page_size#����ȡ��
            current_page=1
            while True:
                #����ƫ����
                offset=(current_page-1)*page_size
                #��ҳ��ѯ
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
                    print("��ԤԼ��¼")
                    return
                #��ʾ����׼��
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
                    #��ӡ
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                        "ԤԼ��¼ID","��ʦID","��ʦ����","ʵ����ID","��ʼʹ��ʱ��","����ʹ��ʱ��"))
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
                    #��ҳ����
                if total_pages>1:
                        action=input("���������:n:��һҳ p:��һҳ j:��תĿ��ҳ q:�˳� ").lower()
                        if action=='n':
                            current_page=min(current_page+1,total_pages)
                        elif action=='p':
                            current_page=max(current_page-1,1)
                        elif action=='j':
                            target=int(input(f"������Ŀ��ҳ(1-{total_pages})"))
                            current_page=max(1,min(target,total_pages))
                        elif action=='q':
                            break
                        else:
                            print("��Ч������")
                else:
                        input("û�и���ҳ,�����������")
                        break
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"����ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def reservation_cancel():#ȡ��δ��ʼ��ԤԼ
            conn = DBPool.get_instance().get_conn()
            cursor = conn.cursor()
            while True:
                TeacherID=input("���������Ľ�ʦID")
                if TeacherID:
                    cursor.execute("SELECT 1 FROM Lab_Reservations WHERE TeacherID=%s",(TeacherID,))
                    if not cursor.fetchone():
                        print("�ý�ʦID��ԤԼ��¼��ý�ʦID������,����������")
                    else:
                        break
                else:
                    print("��ʦID����Ϊ��,����������")
            #��ȡ��ǰʱ��
            DateTime=datetime.today()
            try:
                while True:
                    ReservationID=input("������Ҫȡ����ԤԼ��¼ID")
                    if ReservationID:
                        cursor.execute("SELECT 1 FROM LabReservations WHERE ReservationID=%s",(ReservationID))
                        if not cursor.fetchone():
                            print("��ԤԼ��¼������,����������")
                        else:
                            break
                    else:
                        print("ԤԼ��¼ID����Ϊ��,����������")
                    cursor.execute("SELECT StartTime FROM LabReservations WHERE ReservationID=%s",(ReservationID))
                    re_datetime=cursor.fetchone()
                    if DateTime<re_datetime[0]:
                        cursor.execute("DELETE FROM LabReservations WHERE TeacherID=%s AND ReservationID=%s",(TeacherID,ReservationID,))
                        conn.commit()
                        print("ȡ���ɹ�")
                    else:
                        print("ʱ�䲻�Ϸ�")
            except Exception as e:
                conn.rollback()
                print(f"����ʧ�ܣ�{str(e)}")
            finally:
                cursor.close()
                conn.close()