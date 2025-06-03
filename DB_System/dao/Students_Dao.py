from sqlite3 import Cursor
from openpyxl import Workbook
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
            cursor.execute(sql,(Name, Gender, BirthDate, Phone,))
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
            cursor.execute(sql,(Phone,StudentID,))
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
            cursor.execute("UPDATE Students SET ClassID=%s WHERE StudentID=%s",(ClassID,StudentID,))
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
    def import_from_excel(valid_records):#从excel文件导入学生数据到数据库
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.executemany("INSERT INTO Students(Name,Gender,BirthDate,Phone,ClassID)VALUES(%s,%s,%s,%s,%s)"(valid_records,))
            conn.commit()
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
        # 设置列宽自适应
        for idx, col in enumerate(df.columns):
            max_len = max((
                df[col].astype(str).map(len).max(),  # 列内容最大长度
                len(str(col))  # 列标题长度
            )) + 2  # 额外填充
            worksheet.set_column(idx, idx, max_len)
                
        # 设置标题行格式
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        print(f"导出完成，文件已保存至: {filepath}")


