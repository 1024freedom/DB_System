from sqlalchemy import true
from dao.Att_Ass_Dao import Att_Ass_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
from datetime import date
class Att_Ass_Services:
    @staticmethod
    def Attendance_add():#���ڼ�¼
        while True:
            StudentID = input("������ѧ��ID��").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("��ѧ�������ڣ����������룺")
            else:
                break
        while True:
            CourseID = input("������γ�ID��").strip()
            if not Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                print("�ÿγ̲����ڸ�ѧ���Ŀα��У����������룺")
            else:
                break
        while True:
            Status=input("����������Ŀ���״̬:").strip()
            if Status not in ('����','�ٵ�','ȱ��'):
                print("״̬���Ϸ�,����������")
            else:
                break
        Date=date.today()
        try:
            Att_Ass_Dao.Attendance_add(StudentID,CourseID,Date,Status)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def Assignment_add():#��ҵ����
        while True:
            CourseID=input("���������ҵ�����γ�ID")
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                print("�ÿγ̲�����,����������")
            else:
                break
        while True:
            Title=input("��������ҵ����")
            if Title:
                break
            else:
                print("���ⲻ��Ϊ��")
        #�������ʱ��
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#ʱ���ʽ
        while True:
            Deadline=input("�������ύ��ֹʱ��(��ʽ:2025-12-31 23:34):").strip()
            if not Deadline:
                print("��ֹʱ�䲻��Ϊ��")
                continue
            if not re.match(pattern,Deadline):
                print("��ʽ����,��ʹ��ʾ����ʽ")
            else:
                break
        try:
            Att_Ass_Dao.Assignment_add(CourseID,Title,Deadline)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")