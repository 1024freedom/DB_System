from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import re
import datetime
class Courses_Dao:
    @staticmethod
    def add_courses(CourseName,Credit,TeacherID):#新增课程
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("INSERT INTO Courses (CourseName,Credit,TeacherID) VALUES(%s,%s,%s)"(CourseName,Credit,TeacherID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_name(newCourseName,CourseID):#编辑课程名称
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET CourseName=%s WHERE CourseID=%s"(newCourseName,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_courses_credit(newCredit,CourseID):#编辑课程学分
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET Credit=%s WHERE CourseID=%s"(newCredit,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def edit_teachers(newTeacherID,CourseID):#编辑授课教师
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Courses SET TeacherID=%s WHERE CourseID=%s"(newTeacherID,CourseID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def attach_course_tb(CourseID,TextbookID):#为课程绑定教材
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE FROM Textbooks SET CourseID=%s WHERE TextbookID=%s"(CourseID,TextbookID))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def course_capacity():#课程容量监控 实时显示选课人数与课程最大容量 预警超限情况
        try:
            conn=DBPool.get_instance().get_conn()
            cursor=conn.cursor()
            #容量监控视图
            """CREATE VIEW vw_Course_Capacity AS
                SELECT
                  c.CourseID,
                  c.CourseName,
                  c.Capacity,
                  (c.Capacity-COUNT(e.EnrollmentID)) AS remain
                  FROM Courses c
                  LEFT JOIN Enrollments e ON c.CourseID=e.CourseID
                  GROUP BY c.CourseID
            """
            #获取总记录数
            cursor.execute("SELECT COUNT(*) AS total FROM vw_Course_Capacity ")
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
                                CourseID,
                                CourseName,
                                Capacity,
                                remain
                                FROM vw_Course_Capacity
                                LIMIT %s OFFSET %s
                                """(page_size,offset))
                courses=cursor.fetchall()
                if not courses:
                    print("无课程数据")
                    return
                #显示数据准备
                display_data=[]
               
                for course in courses:
                        capacity=course['Capacity']
                        remain=course['remain']
                        #状态
                        status="正常"
                        if remain/capacity>=0.9:
                            status="预警！"
                        display_data.append({
                            'CourseID':course['CourseID'],
                            'CourseName':course['CourseName'],
                            'Capacity':course['Capacity'],
                            'remain':course['remain'],
                            'status':status
                            })
                    #打印
                print(f"当前页码:{current_page}/{total_pages}")
                print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                        "课程ID","课程名称","容量","余量","状态"))
                print("-"*60)
                for item in display_data:
                        print("{:<10}{:<25}{:<10}{:<10}{:<5}".format(
                            item['CourseID'],
                            item['CourseName'],
                            item['Capacity'],
                            item['remain'],
                            item['status']
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
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def course_time_arr(CourseID,Day,StartTime,EndTime):#排课
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            cursor.execute("UPDATE TABLE SET Day=%s,StartTime=%s,EndTime=%s WHERE CourseID=%s ",(Day,StartTime,EndTime,CourseID,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()