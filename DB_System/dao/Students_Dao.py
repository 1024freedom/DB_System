from sqlite3 import Cursor
from pymysql import NULL
from utils.db_pool import DBPool
import re
import datetime
class Students_Dao:
    @staticmethod
    def add_student_once():#单次增加学生信息
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            Name=input('输入姓名：').strip()#去除空格检验是否非空
            if Name:
                break
            print("姓名不能为空，请重新输入")
        while True:
            Gender=input('输入性别（男/女）：').strip()
            if Gender in ('男','女'):
                break
            print ("请输入正确的性别：")
        data_pattern =re.complie(r'^\d{4}-\d{2}-\d{2}$')#规定格式
        while True:
            BirthDate=input('请输入正确的出生年月日（格式：YYYY-MM-DD').strip()
            if data_pattern.match(BirthDate):
                try:
                    #进一步验证日期的有效性
                    datetime.strptime(BirthDate, '%Y-%m-%d')
                    break
                except ValueError:
                    print("无效的日期，请重新输入")
            else:
                print("日期格式错误，请重新输入：")
        while True:
            Phone=input("请输入手机号：").strip()
            if not Phone:
                Phone=None
                break
            if len(Phone)!=11:
                print("所输入手机号不合法，请重新输入")
                continue
            else:
                cursor.execute("SELECT 1 FROM Students WHERE Phone=%s",(Phone))
            #使用select 1更高效
            if cursor.fetchone():
                print("该手机号已被注册")
            else:
                break
        #验证通过，执行插入
        try:
            sql="""INSERT INTO Students (Name, Gender, BirthDate, Phone)
            VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql,(Name, Gender, BirthDate, Phone))
            conn.commit()
            print("学生信息添加成功")
        except Exception as e:
            conn.rollback()
            print(f"添加失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def alter_student_phone():
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            StudentID=input("请输入学生ID：").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("该学生不存在，请重新输入：")
            else:
                break
        while True:
            Phone=input("请输入手机号：").strip()
            if len(Phone)!=11:
                print("所输入手机号不合法，请重新输入")
                continue
            else:
                cursor.execute("SELECT 1 FROM Students WHERE Phone=%s AND StudentID!=%s",(Phone,StudentID))
            #使用select 1更高效
            if cursor.fetchone():
                print("该手机号已被注册")
            else:
                break
        try:
            sql="""UPDATE Students SET Phone=%s WHERE StudentID=%s"""
            cursor.execute(sql,(Phone,StudentID))
            conn.commit()
            print("学生手机号修改成功！")
        except Exception as e:
            conn.rollback()
            print(f"修改失败：{str(e)}")
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def alter_student_class():
        conn=DBPool.get_instance().get_coon()
        cursor=conn.cursor()
        while True:
            StudentID=input("请输入学生ID：").strip()
            cursor.execute("SELECT 1 FROM Students WHERE StudentID = %s", (StudentID,))
            if not cursor.fetchone():
                print("该学生不存在，请重新输入：")
            else:
                break
        while True:
            ClassID=input("请输入要为该学生分配的班级号：")
            if not ClassID:
                break
            else:
                cursor.execute("SELECT 1 FROM Classes WHERE ClassID=%s",(ClassID))
                if not cursor.hatchone():
                    print("该班级不存在，请重新输入")
                else:
                    cursor.execute("SELECT 1 FROM Classes WHERE ClassID=%s",(ClassID))

        