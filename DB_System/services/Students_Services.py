from itertools import filterfalse
from pickle import FALSE
from numpy import False_
from dao.Students_Dao import Students_Dao
from dao.Askpages_Dao import Askpages_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, false
import pandas as pd
import datetime
import re
class Students_Services:
    @staticmethod
    def add_student_once(Name,Gender,BirthDate,Phone):#��������ѧ����Ϣ
        try:
            data_pattern =re.complie(r'^\d{4}-\d{2}-\d{2}$')#�涨��ʽ
            if data_pattern.match(BirthDate):
                try:
                    #��һ����֤���ڵ���Ч��
                    datetime.strptime(BirthDate, '%Y-%m-%d')
                except ValueError:
                    return False,"��Ч�����ڣ�����������"
            else:
                return False,"���ڸ�ʽ�������������룺"
            if Phone:
                if Search_Dao.search1('Students','Phone',Phone):
                    return False,"���ֻ����ѱ�ע��"
            Students_Dao.add_student_once(Name,Gender,BirthDate,Phone)
            return True,"�����ɹ�"
        except Exception as e:
                return False,f"{str(e)}"
    @staticmethod
    def alter_student_phone(StudentID,Phone):#����ѧ����ϵ��ʽ
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"��ѧ�������ڣ����������룺"
            if Search_Dao.search2('Students','Phone','StudentID',Phone,StudentID):
                return False,"���ֻ����ѱ�ע��"
            Students_Dao.alter_student_phone(Phone,StudentID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def alter_student_class(StudentID,ClassID):#Ϊѧ������༶
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"��ѧ�������ڣ����������룺"
        
            if not Search_Dao.search1('Classes','ClassID',ClassID):
                return False,"�ð༶�����ڣ�����������"
                
            CapacityNow=Fetch_Dao.fetch('CapacityNow','Classes','ClassID',ClassID)
            Capacity=Fetch_Dao.fetch('Capacity','Classes','ClassID',ClassID)
            if CapacityNow<Capacity:
                Students_Dao.alter_student_class(ClassID,StudentID,CapacityNow)
                return True,"�����ɹ�"
            else:
                return False,"�ð༶������������ѡ��"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def delete_student(StudentID):  # ɾ��ѧ����Ϣ
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"��ѧ�������ڣ����������룺"
            Students_Dao.delete_student(StudentID)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def import_from_excel(filepath):#��excel�ļ�����ѧ�����ݵ����ݿ�
        filepath=input("�������ļ��ľ���·��")
        df=pd.read_excel(filepath,engine='openpyxl')
        #����������ϴ��Ԥ����
        valid_records=[]#�洢������֤����Ч��¼
        duplicate_phones=set()#�����ظ����ֻ���
        invalid_class_ids=set()#�洢��Ч�İ༶ID
        #��ѯ�����ֻ�����༶ID
        sql="""SELECT Phone FROM Students"""
        existing_phones={row[0] for row in Fetch_Dao.fetchof(sql)}

        sql="""SELECT DISTINCT ClassID FROM Classes"""
        valid_class_ids={row[0] for row in Fetch_Dao.fetchof(sql)}

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
                Students_Dao.import_from_excel(valid_class_ids)
                return True,"�����ɹ�"
            except Exception as e:
                print(f"����ʧ�ܣ�{str(e)}")
    @staticmethod
    def export_to_excel(filepath):#��excel�ļ���ʽ��������ѧ����Ϣ
        try:
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
            count_sql="""SLEECT COUNT(*) AS total FROM Students"""
            base_sql="""SELECT s.StudentID ѧ��
                                s.Name ����
                                s.Gender �Ա�
                                s.BirthDate ��������
                                s.Phone �绰
                                c.ClassName �����༶
                        FROM Students s LEFT JOIN
                        Classes c ON s.ClassID=c.ClassID
                        LIMIT %s OFFSET %s """
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)
            total_records=results['total_records']
            #��ҳ��ѯ����
            while (current_page-1)*page_size<total_records:
                offset =(current_page-1)*page_size
                try:
                    page_data=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)['data']
                except Exception as e:
                    print(f"��ȡ����ʧ�ܣ�{str(e)}")
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
            # �����п�����Ӧ
            for idx, col in enumerate(df.columns):
                max_len = max((
                    df[col].astype(str).map(len).max(),  # ��������󳤶�
                    len(str(col))  # �б��ⳤ��
                )) + 2  # �������
                worksheet.set_column(idx, idx, max_len)
                
            # ���ñ����и�ʽ
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1
            })
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            print(f"������ɣ��ļ��ѱ�����: {filepath}")
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"