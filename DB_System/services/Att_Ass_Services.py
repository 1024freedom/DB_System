from dao.Att_Ass_Dao import Att_Ass_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
from datetime import date
class Att_Ass_Services:
    @staticmethod
    def Attendance_add(StudentID,CourseID,Status):#考勤记录
       try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"该学生不存在，请重新输入"
            if not Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                return False,"该课程不存在该学生的课表中，请重新输入："
            if Status not in ('出勤','迟到','缺勤'):
                return False,"状态不合法，请重新输入"
            Date=date.today()
            Att_Ass_Dao.Attendance_add(StudentID,CourseID,Date,Status)
            return True,"操作成功"
       except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def Assignment_add(CourseID,Title,Deadline):#作业发布
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"该课程不存在,请重新输入"
            if not Title:
                return False,"标题不能为空"
            #处理截至时间
            pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#时间格式
            if not Deadline:
                return False,"截止时间不能为空"
            if not re.match(pattern,Deadline):
                return False,"格式错误,请使用示例格式"
            Att_Ass_Dao.Assignment_add(CourseID,Title,Deadline)
            return True,"操作成功"
        except Exception as e:
            return False,f"{str(e)}"