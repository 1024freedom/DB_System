from dao.Grades_Dao import Grades_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
class Grades_Services:
    @staticmethod
    def grades_insert_once():#�����ɼ�¼��
        while True:
            StudentID = input("������ѧ��ID��").strip()
            if not Search_Dao.search1('Studnets','StudentID',StudentID):
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
            Score=input("������Ҫ¼ȡ�ĳɼ�����(0~100):")
            if Score>100 or Score<0:
                print("����ĳɼ����Ϸ�,����������")
            else:
                break
        try:
            Grades_Dao.grades_insert_once(StudentID,CourseID,Score)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def grades_alert():#���ɾ�������




