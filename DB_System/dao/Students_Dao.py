from sqlite3 import Cursor
from pymysql import NULL
from utils.db_pool import DBPool
import re
import datetime
class Students_Dao:
    @staticmethod
    def add_student_once():#��������ѧ����Ϣ
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
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
            else:
                cursor.execute("SELECT 1 FROM Students WHERE Phone=%s",(Phone))
            #ʹ��select 1����Ч
            if cursor.fetchone():
                print("���ֻ����ѱ�ע��")
            else:
                break
        #��֤ͨ����ִ�в���
        try:
            sql="""INSERT INTO Students (Name, Gender, BirthDate, Phone)
            VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql,(Name, Gender, BirthDate, Phone))
            conn.commit()
            print("ѧ����Ϣ��ӳɹ�")
        except Exception as e:
            conn.rollback()
            print(f"���ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def alter_student_phone():
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            StudentID=input("������ѧ��ID��").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
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
            if cursor.fetchone():
                print("���ֻ����ѱ�ע��")
            else:
                break
        try:
            sql="""UPDATE Students SET Phone=%s WHERE StudentID=%s"""
            cursor.execute(sql,(Phone,StudentID))
            conn.commit()
            print("ѧ���ֻ����޸ĳɹ���")
        except Exception as e:
            conn.rollback()
            print(f"�޸�ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def alter_student_class():
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            StudentID=input("������ѧ��ID��").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("��ѧ�������ڣ����������룺")
            else:
                break
        while True:
            ClassID=input("������ҪΪ��ѧ������İ༶�ţ�")
            if not ClassID:
                break
            else:
                cursor.execute("SELECT 1 FROM Classes WHERE ClassID=%s",(ClassID))
                if not cursor.hatchone():
                    print("�ð༶�����ڣ�����������")
                else:
                    cursor.execute("SELECT 1 FROM Classes WHERE ClassID=%s",(ClassID))

        