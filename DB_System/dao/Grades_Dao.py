from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Grades_Dao:
    @staticmethod
    def grades_insert_once(StudentID,CourseID,Score):#�����ɼ�¼��
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Grades (StudentID,CourseID,Score) VALUES (%s,%s,%s)"(StudentID,CourseID,Score))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
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


                alerts=cursor.fetchall()
                if not alerts:
                    print("�޾�����Ա")
                    return
                #��ʾ����׼��
                display_data=[]
               
                for alert in alerts:
                    
                        display_data.append({
                            'StudentID':alert['StudentID'],
                            'CourseID':alert['CourseID'],
                            'StudentName':alert['StudentName'],
                            'CourseName':alert['CourseName'],
                            'Score':alert['Score']
                            })
                    #��ӡ
                print(f"��ǰҳ��:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                      "����ѧ��ID","�γ�ID","ѧ������","�γ���","����"))
                print("-"*50)
                for item in display_data:
                        print("{:<10}{:<10}{:<10}{:<10}{:<10}".format(
                            item['StudentID'],
                            item['CourseID'],
                            item['StudentName'],
                            item['CourseName'],
                            item['Score']
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





