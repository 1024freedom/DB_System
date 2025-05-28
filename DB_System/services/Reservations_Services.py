from dao.Reservations_Dao import Reservations_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import date
import re
class Reservation_Services:
    @staticmethod
    def lab_reservation():#ʵ����ԤԼ
        while True:
            TeacherID=input("���������Ľ�ʦID")
            if TeacherID:
                if not Search_Dao.search1('Teachers','TeacherID',TeacherID):
                    print("�ý�ʦID������,����������")
                else:
                    break
            else:
                print("��ʦID����Ϊ��,����������")
        while True:
            LabID=input("������ҪԤԼ��ʵ����ID")
            if LabID:
                if Search_Dao.search1('Classrooms','ClassroomID',LabID):
                    Type=Fetch_Dao.fetch('Type','Classrooms','ClassroomID',LabID)
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
            sql="""SELECT 
                    l.StartTime,
                    l.EndTime 
                    FROM Labreservations l
                    WHERE l.LabID=%s
                """
            params=(LabID)
            exist=False#���ʱ���ͻ
            for(exist_start,exist_end) in Fetch_Dao.fetchof(sql,params):    
                if (StartTime>exist_start and StartTime<exist_end) or (EndTime>exist_start and EndTime<exist_end):
                    print(f"��ʱ���{StartTime}-{EndTime}�ѱ�ԤԼ��������ѡ��")
                    exist=True
                    break
            if not exist:
                break
        try:
            Reservations_Dao.lab_reservation(LabID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")