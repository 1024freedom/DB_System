from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Grades_Dao:
    def grades_insert_once():#�����ɼ�¼��
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        while True:
            StudentID = input("������ѧ��ID��").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("��ѧ�������ڣ����������룺")
            else:
                break
        while True:
            CourseID = input("������γ�ID��").strip()
            cursor.execute("SELECT 1 FROM Enrollments WHERE CourseID = %s ADD StudentID=%s", (CourseID,StudentID))
            if not cursor.fetchone():
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
            cursor.execute("INSERT INTO Grades (StudentID,CourseID,Score) VALUES (%s,%s,%s)"(StudentID,CourseID,Score))
            conn.commit()
            print("¼��ɹ�")
        except Exception as e:
            conn.rollback()
            print(f"¼��ʧ�ܣ�{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def grades_alert():#���ɾ�������
        
        try:
            conn = DBPool.get_instance().get_conn()
            cursor = conn.cursor()
            #�ɼ�������ͼ
            """CREATE VIEW vw_Grades_Alert AS
                        SELECT 
                            g.StudentID,
                            g.CourseID,
                            s.Name AS StudentName,
                            c.CourseName,
                            g.Score
                        FROM Grades g
                        JOIN Students s ON g.StudentID=s.StudentID
                        JOIN Courses c ON g.CourseID=c.CourseID
                        WHERE g.Score<60
            """
            cursor.execute("SELECT COUNT(*) AS total FROM vw_Grades_Alert ")
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
                                StudentID,
                                CourseID,
                                StudentName,
                                CourseName,
                                Score
                                FROM vw_Grades_Alert
                                LIMIT %s OFFSET %s
                                """(page_size,offset))


                enrollments=cursor.fetchall()
                if not enrollments:
                    print("�޾�����Ա")
                    return
                #��ʾ����׼��
                display_data=[]
               
                for enrollment in enrollments:
                    
                        display_data.append({
                            'StudentID':enrollment['StudentID'],
                            'CourseID':enrollment['CourseID'],
                            'StudentName':enrollment['StudentName'],
                            'CourseName':enrollment['CourseName'],
                            'Score':
                            })
                    #��ӡ
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                        "ѡ�μ�¼ID","ѧ��ID","ѧ������","�γ�ID","�γ���","�ڿν�ʦ","����","�Ͽ�ʱ��","�¿�ʱ��"))
                print("-"*95)
                for item in display_data:
                        print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                            item['EnrollmentID'],
                            item['StudentID'],
                            item['StudentName'],
                            item['CourseID'],
                            item['CourseName'],
                            item['TeacherName'],
                            item['Day'],
                            item['StartTime'],
                            item['EndTime']
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





