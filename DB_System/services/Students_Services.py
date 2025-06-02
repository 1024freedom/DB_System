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
    def add_student_once(Name,Gender,BirthDate,Phone):#单次增加学生信息
        try:
            data_pattern =re.complie(r'^\d{4}-\d{2}-\d{2}$')#规定格式
            if data_pattern.match(BirthDate):
                try:
                    #进一步验证日期的有效性
                    datetime.strptime(BirthDate, '%Y-%m-%d')
                except ValueError:
                    return False,"无效的日期，请重新输入"
            else:
                return False,"日期格式错误，请重新输入："
            if Phone:
                if Search_Dao.search1('Students','Phone',Phone):
                    return False,"该手机号已被注册"
            Students_Dao.add_student_once(Name,Gender,BirthDate,Phone)
            return True,"操作成功"
        except Exception as e:
                return False,f"{str(e)}"
    @staticmethod
    def alter_student_phone(StudentID,Phone):#更改学生联系方式
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"该学生不存在，请重新输入："
            if Search_Dao.search2('Students','Phone','StudentID',Phone,StudentID):
                return False,"该手机号已被注册"
            Students_Dao.alter_student_phone(Phone,StudentID)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def alter_student_class(StudentID,ClassID):#为学生分配班级
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"该学生不存在，请重新输入："
        
            if not Search_Dao.search1('Classes','ClassID',ClassID):
                return False,"该班级不存在，请重新输入"
                
            CapacityNow=Fetch_Dao.fetch('CapacityNow','Classes','ClassID',ClassID)
            Capacity=Fetch_Dao.fetch('Capacity','Classes','ClassID',ClassID)
            if CapacityNow<Capacity:
                Students_Dao.alter_student_class(ClassID,StudentID,CapacityNow)
                return True,"操作成功"
            else:
                return False,"该班级已满，请重新选择"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def delete_student(StudentID):  # 删除学生信息
        try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"该学生不存在，请重新输入："
            Students_Dao.delete_student(StudentID)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def import_from_excel(filepath):#从excel文件导入学生数据到数据库
        filepath=input("请输入文件的绝对路径")
        df=pd.read_excel(filepath,engine='openpyxl')
        #进行数据清洗与预处理
        valid_records=[]#存储经过验证的有效记录
        duplicate_phones=set()#跟踪重复的手机号
        invalid_class_ids=set()#存储无效的班级ID
        #查询现有手机号与班级ID
        sql="""SELECT Phone FROM Students"""
        existing_phones={row[0] for row in Fetch_Dao.fetchof(sql)}

        sql="""SELECT DISTINCT ClassID FROM Classes"""
        valid_class_ids={row[0] for row in Fetch_Dao.fetchof(sql)}

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
                Students_Dao.import_from_excel(valid_class_ids)
                return True,"操作成功"
            except Exception as e:
                print(f"操作失败：{str(e)}")
    @staticmethod
    def export_to_excel(filepath):#以excel文件形式批量导出学生信息
        try:
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
            count_sql="""SLEECT COUNT(*) AS total FROM Students"""
            base_sql="""SELECT s.StudentID 学号
                                s.Name 姓名
                                s.Gender 性别
                                s.BirthDate 出生日期
                                s.Phone 电话
                                c.ClassName 所属班级
                        FROM Students s LEFT JOIN
                        Classes c ON s.ClassID=c.ClassID
                        LIMIT %s OFFSET %s """
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)
            total_records=results['total_records']
            #分页查询数据
            while (current_page-1)*page_size<total_records:
                offset =(current_page-1)*page_size
                try:
                    page_data=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)['data']
                except Exception as e:
                    print(f"获取数据失败：{str(e)}")
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
            return True,"导出成功"
        except Exception as e:
            return False,f"{str(e)}"