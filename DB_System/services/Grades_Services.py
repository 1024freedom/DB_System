from dao.Grades_Dao import Grades_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
class Grades_Services:
    @staticmethod
    def grades_insert_once():#单条成绩录入
        while True:
            StudentID = input("请输入学生ID：").strip()
            if not Search_Dao.search1('Studnets','StudentID',StudentID):
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
            Score=input("请输入要录取的成绩分数(0~100):")
            if Score>100 or Score<0:
                print("输入的成绩不合法,请重新输入")
            else:
                break
        try:
            Grades_Dao.grades_insert_once(StudentID,CourseID,Score)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")
    @staticmethod
    def grades_alert():#生成警告名单




