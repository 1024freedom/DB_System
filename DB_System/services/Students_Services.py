from dao.Students_Dao import Students_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
class Students_Services:
    @staticmethod
    def add_student_once():#单次增加学生信息
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
            elif Search_Dao.search1('Students','Phone',Phone):
                print("该手机号已被注册")
            else:
                break
        #验证通过，执行插入
        try:
            Students_Dao.add_student_once(Name,Gender,BirthDate,Phone)
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def alter_student_phone():#更改学生联系方式
        while True:
            StudentID=input("请输入学生ID：").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
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
            if Search_Dao.search2('Students','Phone','StudentID',Phone,StudentID):
                print("该手机号已被注册")
            else:
                break
        try:
            Students_Dao.alter_student_phone(Phone,StudentID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def alter_student_class():#为学生分配班级
        while True:
            StudentID=input("请输入学生ID：").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("该学生不存在，请重新输入：")
            else:
                break
        while True:
            ClassID=input("请输入要为该学生分配的班级号：")
            if not ClassID:
                print("班级号不能为空，请重新输入")
            else:
                if not Search_Dao.search1('Classes','ClassID',ClassID):
                    print("该班级不存在，请重新输入")
                else:
                    CapacityNow=Fetch_Dao.fetch('CapacityNow','Classes','ClassID',ClassID)
                    Capacity=Fetch_Dao.fetch('Capacity','Classes','ClassID',ClassID)
                    if CapacityNow<Capacity:
                        try:
                            Students_Dao.alter_student_class(ClassID,StudentID,CapacityNow)
                            return True,"操作成功"
                        except Exception as e:
                            print(f"操作失败：{str(e)}")
                        break
                    else:
                        print("该班级已满，请重新选择")
    @staticmethod
    def delete_student():  # 删除学生信息
        while True:
            StudentID = input("请输入学生ID：").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("该学生不存在，请重新输入：")
            else:
                break
        try:
            Students_Dao.delete_student(StudentID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def import_from_excel():#从excel文件导入学生数据到数据库
        filepath=input("请输入文件的绝对路径")
        try:
            Students_Dao.import_from_excel(filepath)
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def export_to_excel():
        filepath=input("请输入导出路径")
        try:
            Students_Dao.export_to_excel(filepath)
        except Exception as e:
            print(f"操作失败：{str(e)}")