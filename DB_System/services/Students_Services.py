from dao.Students_Dao import Students_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
class Students_Services:
    @staticmethod
    def add_student_once():#��������ѧ����Ϣ
        while True:
            Name=input('����������').strip()#ȥ���ո�����Ƿ�ǿ�
            if Name:
                break
            print("��������Ϊ�գ�����������")
        while True:
            Gender=input('�����Ա���/Ů����').strip()
            if Gender in ('��','Ů'):
                break
            print ("��������ȷ���Ա�")
        data_pattern =re.complie(r'^\d{4}-\d{2}-\d{2}$')#�涨��ʽ
        while True:
            BirthDate=input('��������ȷ�ĳ��������գ���ʽ��YYYY-MM-DD').strip()
            if data_pattern.match(BirthDate):
                try:
                    #��һ����֤���ڵ���Ч��
                    datetime.strptime(BirthDate, '%Y-%m-%d')
                    break
                except ValueError:
                    print("��Ч�����ڣ�����������")
            else:
                print("���ڸ�ʽ�������������룺")
        while True:
            Phone=input("�������ֻ��ţ�").strip()
            if not Phone:
                Phone=None
                break
            if len(Phone)!=11:
                print("�������ֻ��Ų��Ϸ�������������")
                continue
            elif Search_Dao.search1('Students','Phone',Phone):
                print("���ֻ����ѱ�ע��")
            else:
                break
        #��֤ͨ����ִ�в���
        try:
            Students_Dao.add_student_once(Name,Gender,BirthDate,Phone)
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def alter_student_phone():#����ѧ����ϵ��ʽ
        while True:
            StudentID=input("������ѧ��ID��").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("��ѧ�������ڣ����������룺")
            else:
                break
        while True:
            Phone=input("�������ֻ��ţ�").strip()
            if len(Phone)!=11:
                print("�������ֻ��Ų��Ϸ�������������")
                continue
            else:
                cursor.execute("SELECT 1 FROM Students WHERE Phone=%s AND StudentID!=%s",(Phone,StudentID))
            #ʹ��select 1����Ч
            if Search_Dao.search2('Students','Phone','StudentID',Phone,StudentID):
                print("���ֻ����ѱ�ע��")
            else:
                break
        try:
            Students_Dao.alter_student_phone(Phone,StudentID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def alter_student_class():#Ϊѧ������༶
        while True:
            StudentID=input("������ѧ��ID��").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("��ѧ�������ڣ����������룺")
            else:
                break
        while True:
            ClassID=input("������ҪΪ��ѧ������İ༶�ţ�")
            if not ClassID:
                print("�༶�Ų���Ϊ�գ�����������")
            else:
                if not Search_Dao.search1('Classes','ClassID',ClassID):
                    print("�ð༶�����ڣ�����������")
                else:
                    CapacityNow=Fetch_Dao.fetch('CapacityNow','Classes','ClassID',ClassID)
                    Capacity=Fetch_Dao.fetch('Capacity','Classes','ClassID',ClassID)
                    if CapacityNow<Capacity:
                        try:
                            Students_Dao.alter_student_class(ClassID,StudentID,CapacityNow)
                            return True,"�����ɹ�"
                        except Exception as e:
                            print(f"����ʧ�ܣ�{str(e)}")
                        break
                    else:
                        print("�ð༶������������ѡ��")
    @staticmethod
    def delete_student():  # ɾ��ѧ����Ϣ
        while True:
            StudentID = input("������ѧ��ID��").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("��ѧ�������ڣ����������룺")
            else:
                break
        try:
            Students_Dao.delete_student(StudentID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def import_from_excel():#��excel�ļ�����ѧ�����ݵ����ݿ�
        filepath=input("�������ļ��ľ���·��")
        try:
            Students_Dao.import_from_excel(filepath)
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def export_to_excel():
        filepath=input("�����뵼��·��")
        try:
            Students_Dao.export_to_excel(filepath)
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")