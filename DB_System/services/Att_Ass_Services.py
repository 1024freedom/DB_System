from sqlalchemy import true
from dao.Att_Ass_Dao import Att_Ass_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
from datetime import date
class Att_Ass_Services:
    @staticmethod
    def Attendance_add():#考勤记录
        while True:
            StudentID = input("请输入学生ID：").strip()
            if not Search_Dao.search1('Students','StudentID',StudentID):
                print("该学生不存在，请重新输入：")
            else:
                break
        while True:
            CourseID = input("请输入课程ID：").strip()
            if not Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                print("该课程不存在该学生的课表中，请重新输入：")
            else:
                break
        while True:
            Status=input("请输入该生的考勤状态:").strip()
            if Status not in ('出勤','迟到','缺勤'):
                print("状态不合法,请重新输入")
            else:
                break
        Date=date.today()
        try:
            Att_Ass_Dao.Attendance_add(StudentID,CourseID,Date,Status)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def Assignment_add():#作业发布
        while True:
            CourseID=input("请输入该作业关联课程ID")
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                print("该课程不存在,请重新输入")
            else:
                break
        while True:
            Title=input("请输入作业标题")
            if Title:
                break
            else:
                print("标题不能为空")
        #处理截至时间
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#时间格式
        while True:
            Deadline=input("请输入提交截止时间(格式:2025-12-31 23:34):").strip()
            if not Deadline:
                print("截止时间不能为空")
                continue
            if not re.match(pattern,Deadline):
                print("格式错误,请使用示例格式")
            else:
                break
        try:
            Att_Ass_Dao.Assignment_add(CourseID,Title,Deadline)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")