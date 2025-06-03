from dao.Grades_Dao import Grades_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from dao.Askpages_Dao import Askpages_Dao
import datetime
import re
class Grades_Services:
    @staticmethod
    def grades_insert_once(StudentID,CourseID,Score):#单条成绩录入
        try:
            if not Search_Dao.search1('Studnets','StudentID',StudentID):
                return False,"该学生不存在，请重新输入："
            if not Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                return False,"该课程不存在该学生的课表中，请重新输入："
            Grades_Dao.grades_insert_once(StudentID,CourseID,Score)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def grades_alert(current_page):#生成警告名单
        
        base_sql="""SELECT
                        StudentID,
                        CourseID,
                        StudentName,
                        CourseName,
                        Score
                        FROM vw_Grades_Alert
                        LIMIT %s OFFSET %s
        """
        count_sql="""SELECT COUNT(*) AS total FROM vw_Grades_Alert 
        """
        page_size=20
        try:
            results=Askpages_Dao.ask(base_sql,count_sql,page_size,current_page)
            #显示数据准备
               
            #(显示逻辑处理)
            #for item in results['data']:
                    
            return True,results
        except Exception as e:
            return False,f"{str(e)}"


