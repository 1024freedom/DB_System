from dao.Enrollments_Dao import Enrollments_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
class Enrollments_Servises:
    @staticmethod
    def students_enroll():#学生选课

    @staticmethod
    def students_drop_course():#学生退课
        while True:
            StudentID=input("请输入学号").strip()
            if StudentID:
                if not Search_Dao.search1('Enrollments','StudentID',StudentID):
                    print("选课记录中不存在该学号，请重新输入")
                else:
                    break
            else:
                print("学号不能为空，请重新输入")
        while True:
            CourseID=input("请输入要退选的课程ID").strip()
            if CourseID:
                if not Search_Dao.search2('Enrollments','StudentID','CourseID',StudentID,CourseID):
                    print("选课记录中不存在该课程，请重新输入")
                else:
                    break
            else:
                print("课程号不能为空，请重新输入")
        try:
            Enrollments_Dao.students_drop_course(StudentID,CourseID)
            return True,"操作成功"
        except Exception as e:
            print(f"操作失败：{str(e)}")



