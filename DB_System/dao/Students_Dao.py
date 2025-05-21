from sqlite3 import Cursor
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
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
            #ʹ��select 1����Ч,��ʽ����ֹSQLע��
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
    def alter_student_phone():#����ѧ����ϵ��ʽ
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
    def alter_student_class():#Ϊѧ������༶
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
                    cursor.execute("SELECT CapacityNow,Capacity FROM Classes WHERE ClassID=%s",(ClassID))
                    CapacityNow,Capacity=cursor.fetchone()
                    if CapacityNow<Capacity:
                        try:
                            cursor.execute("UPDATE Students SET ClassID=%s WHERE StudentID=%s",(ClassID,StudentID))
                            cursor.execute("UPDATE Classer SET CapacityNow=%s+1 WHERE ClassID=%s",(CapacityNow,ClassID,))
                            conn.commit()
                            print("����༶�ɹ�")
                        except Exception as e:
                            conn.rollback()
                            print(f"����ʧ�ܣ�{str(e)}")
                        finally:
                            cursor.close()
                            conn.close()
    @staticmethod
    def delete_student():  # ɾ��ѧ����Ϣ
        conn = DBPool.get_instance().get_coon()
        cursor = conn.cursor()
    
        while True:
            StudentID = input("������ѧ��ID��").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("��ѧ�������ڣ����������룺")
            else:
                break
    
        try:
            cursor.execute("DELETE FROM Students WHERE StudentID=%s", (StudentID,))
            conn.commit()
            print("ɾ���ɹ�")
        except Exception as e:
            conn.rollback()
            print(f"ɾ��ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def import_from_excel():#��excel�ļ�����ѧ�����ݵ����ݿ�
        conn = DBPool.get_instance().get_coon()
        cursor = conn.cursor()
        filepath=input("�������ļ��ľ���·��")
        df=pd.read_excel(filepath,engine='openpyxl')
        #����������ϴ��Ԥ����
        valid_records=[]#�洢������֤����Ч��¼
        duplicate_phones=set()#�����ظ����ֻ���
        invalid_class_ids=set()#�洢��Ч�İ༶ID
        #��ѯ�����ֻ�����༶ID
        cursor.execute("SELECT Phone FROM Students")
        existing_phones={row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT DISTINCT ClassID FROM Classes")
        valid_class_ids={row[0] for row in cursor.fatchall()}

        #��������
        for index,row in df.iterrows():
            #��ֵУ��
            if pd.isnull(row['Name']) or pd.isnull(row['Gender']) or pd.isnull(['BirthDate']):
                print(f'��{index+2}��ȱʧ���ݣ�������')
                continue

            #�Ա�У��
            gender=str(row['Gender']).strip()
            if gender not in('��','Ů'):
                print(f'��{index+2}���Ա�ֵ���Ϸ���������')
                continue

            #�ֻ���У��
            phone =str(row['Phone']).strip().replace(' ','')if not pd.isnull(row['Phone'])else None
            if phone:
                if phone in existing_phones:
                    print(f'��{index+2}���ֻ����Ѵ��ڣ�����������')
                    duplicate_phones.add(phone)
                    continue
                existing_phones.add(phone)
            #�༶IDУ��
            class_id =row['ClassID']
            if class_id and class_id not in valid_class_ids:
                invalid_class_ids.add(class_id)
                print(f'��{index+2}�а༶�Ų����ڣ�������')
                continue

            #���ڸ�ʽת��
            birth_date =pd.to_datatime(row['BirthDate']).strftime('%Y-%m-%d')
            valid_records.append((
                row['Name'],#���ȡ
                gender,
                birth_date,
                phone,
                class_id
                ))
        if valid_records:
            try:
                cursor.execute("INSERT INTO Students(Name,Gender,BirthDate,Phone,ClassID)VALUES(%s,%s,%s,%s,%s)"(valid_records))
                conn.commit()
                print(f"�ɹ�����{len(valid_records)}����¼")
            except Exception as e:
                conn.rollback()
                print(f"����ʧ�ܣ�{str(e)}")
            finally:
                cursor.close()
                conn.close() 
    @staticmethod
    def export_to_excel():
        conn = DBPool.get_instance().get_coon()
        cursor = conn.cursor()


