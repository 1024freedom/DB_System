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
    def add_student_once(Name,Gender,BirthDate,Phone):#单次增加学生信息
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        #验证通过，执行插入
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
    def alter_student_phone(Phone,StudentID):#更改学生联系方式
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            sql="""UPDATE Students SET Phone=%s WHERE StudentID=%s"""
            cursor.execute(sql,(Phone,StudentID))
            conn.commit()
            print("学生手机号修改成功！")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def alter_student_class(ClassID,StudentID,CapacityNow):#为学生分配班级
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
    def delete_student(StudentID):  # 删除学生信息
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
    def import_from_excel(filepath):#从excel文件导入学生数据到数据库
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        df=pd.read_excel(filepath,engine='openpyxl')
        #进行数据清洗与预处理
        valid_records=[]#存储经过验证的有效记录
        duplicate_phones=set()#跟踪重复的手机号
        invalid_class_ids=set()#存储无效的班级ID
        #查询现有手机号与班级ID
        cursor.execute("SELECT Phone FROM Students")
        existing_phones={row[0] for row in cursor.fetchall()}

        cursor.execute("SELECT DISTINCT ClassID FROM Classes")
        valid_class_ids={row[0] for row in cursor.fatchall()}

        #遍历数据
        for index,row in df.iterrows():
            #空值校验
            if pd.isnull(row['Name']) or pd.isnull(row['Gender']) or pd.isnull(['BirthDate']):
                print(f'第{index+2}行缺失数据，已跳过')
                continue

            #性别校验
            gender=str(row['Gender']).strip()
            if gender not in('男','女'):
                print(f'第{index+2}行性别值不合法，已跳过')
                continue

            #手机号校验
            phone =str(row['Phone']).strip().replace(' ','')if not pd.isnull(row['Phone'])else None
            if phone:
                if phone in existing_phones:
                    print(f'第{index+2}行手机号已存在，已跳过该行')
                    duplicate_phones.add(phone)
                    continue
                existing_phones.add(phone)
            #班级ID校验
            class_id =row['ClassID']
            if class_id and class_id not in valid_class_ids:
                invalid_class_ids.add(class_id)
                print(f'第{index+2}行班级号不存在，已跳过')
                continue

            #日期格式转换
            birth_date =pd.to_datatime(row['BirthDate']).strftime('%Y-%m-%d')
            valid_records.append((
                row['Name'],#需获取
                gender,
                birth_date,
                phone,
                class_id
                ))
        if valid_records:
            try:
                cursor.execute("INSERT INTO Students(Name,Gender,BirthDate,Phone,ClassID)VALUES(%s,%s,%s,%s,%s)"(valid_records))
                conn.commit()
                print(f"成功导入{len(valid_records)}条记录")
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
        #文件名具有时效性
        timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename=f"students_export_{timestamp}.xlsx"
        if not filepath:
            filepath=default_filename#若不输入路径，则会导出到当前目录

        #检查扩展名
        if not filepath.lower().endswith('.xlsx'):
            filepath+='.xlsx'

        #分页参数
        page_size=5000#每页查询的数据量
        current_page=1
        all_data=[]
        #获取总记录数
        cursor.execute("SLEECT COUNT(*) total FROM Students")
        total=cursor.fetchone()['total']
        print(f'一共{total}条记录，现在开始导出.....')

        #分页查询数据
        while (current_page-1)*page_size<total:
            offset =(current_page-1)*page_size
            cursor.execute("""SELECT s.StudentID 学号
                                     s.Name 姓名
                                     s.Gender 性别
                                     s.BirthDate 出生日期
                                     s.Phone 电话
                                     c.ClassName 所属班级
                               FROM Students s LEFT JOIN
                               Classes c ON s.ClassID=c.ClassID
                               LIMIT %s OFFSET %s """(page_size,offset))
            page_data=cursor.fetchall()
            all_data.extend(page_data)#注意用extend
            if all_data:
                current_page+=1
                print(f"已加载一页数据到内存")
            else:
                 print ("没有可以导出的数据")
                 return 

        #转换为DataFrame
        df= pd.DataFrame(all_data)
        #excel写入参数
        writer=pd.ExcelWriter(
            filepath,
            engine='xlsxwriter',
            datetime_format='yyyy-mm-dd',#注意遵循excel的格式规范
            options={'string_to_urls':False}#禁止将特定格式的字符串自动转换为Excel超链接
            )
        df.to_excel(writer,index=False,sheet_name='学生信息')

        #获取工作表对象进行excel表的格式设置
        workbook=writer.book
        worksheet=writer.sheets['学生信息']



