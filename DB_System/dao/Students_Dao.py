from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Students_Dao:
    @staticmethod
    def add_student_once(Name,Gender,BirthDate,Phone):#��������ѧ����Ϣ
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        #��֤ͨ����ִ�в���
        try:
            sql="""INSERT INTO Students (Name, Gender, BirthDate, Phone)
            VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql,(Name, Gender, BirthDate, Phone))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def alter_student_phone(Phone,StudentID):#����ѧ����ϵ��ʽ
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            sql="""UPDATE Students SET Phone=%s WHERE StudentID=%s"""
            cursor.execute(sql,(Phone,StudentID))
            conn.commit()
            print("ѧ���ֻ����޸ĳɹ���")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def alter_student_class(ClassID,StudentID,CapacityNow):#Ϊѧ������༶
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()

        try:
            cursor.execute("UPDATE Students SET ClassID=%s WHERE StudentID=%s",(ClassID,StudentID))
            cursor.execute("UPDATE Classer SET CapacityNow=%s+1 WHERE ClassID=%s",(CapacityNow,ClassID,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def delete_student(StudentID):  # ɾ��ѧ����Ϣ
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Students WHERE StudentID=%s", (StudentID,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def import_from_excel(filepath):#��excel�ļ�����ѧ�����ݵ����ݿ�
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
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
                raise e
            finally:
                cursor.close()
                conn.close() 
    @staticmethod
    def export_to_excel(filepath):
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        #�ļ�������ʱЧ��
        timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename=f"students_export_{timestamp}.xlsx"
        if not filepath:
            filepath=default_filename#��������·������ᵼ������ǰĿ¼

        #�����չ��
        if not filepath.lower().endswith('.xlsx'):
            filepath+='.xlsx'

        #��ҳ����
        page_size=5000#ÿҳ��ѯ��������
        current_page=1
        all_data=[]
        #��ȡ�ܼ�¼��
        cursor.execute("SLEECT COUNT(*) total FROM Students")
        total=cursor.fetchone()['total']
        print(f'һ��{total}����¼�����ڿ�ʼ����.....')

        #��ҳ��ѯ����
        while (current_page-1)*page_size<total:
            offset =(current_page-1)*page_size
            cursor.execute("""SELECT s.StudentID ѧ��
                                     s.Name ����
                                     s.Gender �Ա�
                                     s.BirthDate ��������
                                     s.Phone �绰
                                     c.ClassName �����༶
                               FROM Students s LEFT JOIN
                               Classes c ON s.ClassID=c.ClassID
                               LIMIT %s OFFSET %s """(page_size,offset))
            page_data=cursor.fetchall()
            all_data.extend(page_data)#ע����extend
            if all_data:
                current_page+=1
                print(f"�Ѽ���һҳ���ݵ��ڴ�")
            else:
                 print ("û�п��Ե���������")
                 return 

        #ת��ΪDataFrame
        df= pd.DataFrame(all_data)
        #excelд�����
        writer=pd.ExcelWriter(
            filepath,
            engine='xlsxwriter',
            datetime_format='yyyy-mm-dd',#ע����ѭexcel�ĸ�ʽ�淶
            options={'string_to_urls':False}#��ֹ���ض���ʽ���ַ����Զ�ת��ΪExcel������
            )
        df.to_excel(writer,index=False,sheet_name='ѧ����Ϣ')

        #��ȡ������������excel��ĸ�ʽ����
        workbook=writer.book
        worksheet=writer.sheets['ѧ����Ϣ']



