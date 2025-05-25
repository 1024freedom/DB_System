from sqlite3 import Cursor
from openpyxl import Workbook
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine, true
import pandas as pd
import re
import datetime
class Grades_Dao:
    def grades_insert_once():#单条成绩录入
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        while True:
            StudentID = input("请输入学生ID：").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("该学生不存在，请重新输入：")
            else:
                break
        while True:
            CourseID = input("请输入课程ID：").strip()
            cursor.execute("SELECT 1 FROM Enrollments WHERE CourseID = %s ADD StudentID=%s", (CourseID,StudentID))
            if not cursor.fetchone():
                print("该课程不存在该学生的课表中，请重新输入：")
            else:
                break
        while True:
            Score=input("请输入要录取的成绩分数(0~100):")
            if Score>100 or Score<0:
                print("输入的成绩不合法,请重新输入")
            else:
                break
        try:
            cursor.execute("INSERT INTO Grades (StudentID,CourseID,Score) VALUES (%s,%s,%s)"(StudentID,CourseID,Score))
            conn.commit()
            print("录入成功")
        except Exception as e:
            conn.rollback()
            print(f"录入失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    def grades_alert():#生成警告名单
        
        try:
            conn = DBPool.get_instance().get_conn()
            cursor = conn.cursor()
            #成绩警告视图
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
                print("当前没有数据")
                return
            #设置分页参数
            page_size=20#默认每页显示20条
            total_pages=(total_records+page_size-1)//page_size#向上取整
            current_page=1
            while True:
                #计算偏移量
                offset=(current_page-1)*page_size
                #分页查询
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
                    print("无警告人员")
                    return
                #显示数据准备
                display_data=[]
               
                for enrollment in enrollments:
                    
                        display_data.append({
                            'StudentID':enrollment['StudentID'],
                            'CourseID':enrollment['CourseID'],
                            'StudentName':enrollment['StudentName'],
                            'CourseName':enrollment['CourseName'],
                            'Score':
                            })
                    #打印
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<10}{:<10}{:<10}{:<10}{:10}{:<5}{:<15}{:<15}".format(
                        "选课记录ID","学生ID","学生姓名","课程ID","课程名","授课教师","星期","上课时间","下课时间"))
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
                    #分页导航
                if total_pages>1:
                        action=input("请输入操作:n:下一页 p:下一页 j:跳转目标页 q:退出 ").lower()
                        if action=='n':
                            current_page=min(current_page+1,total_pages)
                        elif action=='p':
                            current_page=max(current_page-1,1)
                        elif action=='j':
                            target=int(input(f"请输入目标页(1-{total_pages})"))
                            current_page=max(1,min(target,total_pages))
                        elif action=='q':
                            break
                        else:
                            print("无效操作码")
                else:
                        input("没有更多页,按任意键返回")
                        break
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"操作失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()





