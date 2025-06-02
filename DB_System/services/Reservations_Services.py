from pickle import FALSE
from numpy import False_
from sqlalchemy import false
from dao.Reservations_Dao import Reservations_Dao
from dao.Askpages_Dao import Askpages_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import datetime
import re
class Reservation_Services:
    @staticmethod
    def lab_reservation(TeacherID,LabID,StartTime,EndTime):#ʵ����ԤԼ
        try:
            if not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                return False,"�ý�ʦID������,����������"
            if Search_Dao.search1('Classrooms','ClassroomID',LabID):
                Type=Fetch_Dao.fetch('Type','Classrooms','ClassroomID',LabID)
                if Type[0]!="ʵ����":
                    return False,"�÷��䲻��ʵ����,����������"
            else:
                return False,"�÷��䲻����,����������"
            pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#ʱ���ʽ
            if not re.match(pattern,StartTime):
                return False,"��ʽ����,��ʹ��ʾ����ʽ"
            if not re.match(pattern,EndTime):
                return False,"��ʽ����,��ʹ��ʾ����ʽ"
            sql="""SELECT 
                    l.StartTime,
                    l.EndTime 
                    FROM Labreservations l
                    WHERE l.LabID=%s
                """
            params=(LabID)
            for(exist_start,exist_end) in Fetch_Dao.fetchof(sql,params):    
                if (StartTime>exist_start and StartTime<exist_end) or (EndTime>exist_start and EndTime<exist_end):
                    return False,f"��ʱ���{StartTime}-{EndTime}�ѱ�ԤԼ��������ѡ��"
            Reservations_Dao.lab_reservation(LabID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def reservation_ask(current_page,ID):#ԤԼ��¼��ѯ
        #ԤԼ��¼��ͼ
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
        #��ҳ����
        page_size=20
        try:
            if not Search_Dao.search1('vw_Lab_Reservations','TeacherID',ID):
                return False,"�ý�ʦID��ԤԼ��¼��ý�ʦID������,����������"
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page,ID)
            #��ʾ����׼��
               
            #(��ʾ�߼�����)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def reservation_cancel(TeacherID,ReservationID):#ȡ��δ��ʼ��ԤԼ
            if not Search_Dao.search1('vw_Lab_Reservations','TeacherID',TeacherID):
                return False,"�ý�ʦID��ԤԼ��¼��ý�ʦID������,����������"
            #��ȡ��ǰʱ��
            DateTime=datetime.today()
            if not Search_Dao.search1('LabReservations','ReservationID',ReservationID):
                return False,"��ԤԼ��¼������,����������"
                
            re_datetime=Fetch_Dao.fetch('StartTime','LabReservations','ReservationID',ReservationID)
            if DateTime<re_datetime[0]:
                try:
                    Reservations_Dao.reservation_cancel(TeacherID,ReservationID)
                    return True,"�����ɹ�"
                except Exception as e:
                    return False,f"{str(e)}"
            else:
                return False,"ʱ�䲻�Ϸ�"