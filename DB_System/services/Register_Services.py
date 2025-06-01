from math import e
from dao.Register_Dao import Register_Dao
from dao.Search_Dao import Search_Dao
from utils.Security_tools import Security_tools
class Register_Services:
    @staticmethod
    def register_student(user_id,password):#学生用户注册
        try:
            if not Search_Dao.search1('Students','StudentID',user_id):
                return False,"该ID无学籍"
            elif not Security_tools.is_password_strong(password):
                return False,"密码强度弱，请重新设置密码"
            else:
                Register_Dao.register_student(user_id,password)
                return True,"注册成功"
        except Exception as e:
            return False,"操作失败"
            return False
    @staticmethod
    def register_student(user_id,password):#学生用户注册
        try:
            if not Search_Dao.search1('Students','StudentID',user_id):
                return False,"该ID无教师籍"
            elif not Security_tools.is_password_strong(password):
                return False,"密码强度弱，请重新设置密码"
            else:
                Register_Dao.register_teacher(user_id,password)
                return True,"注册成功"
        except Exception as e:
            return False,"操作失败"
            return False



