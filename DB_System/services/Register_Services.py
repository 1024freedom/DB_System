from math import e
from dao.Register_Dao import Register_Dao
from dao.Search_Dao import Search_Dao
from utils.Security_tools import Security_tools
class Register_Services:
    @staticmethod
    def register_student(user_id,password):#ѧ���û�ע��
        try:
            if not Search_Dao.search1('Students','StudentID',user_id):
                return False,"��ID��ѧ��"
            elif not Security_tools.is_password_strong(password):
                return False,"����ǿ��������������������"
            else:
                Register_Dao.register_student(user_id,password)
                return True,"ע��ɹ�"
        except Exception as e:
            return False,"����ʧ��"
            return False
    @staticmethod
    def register_student(user_id,password):#ѧ���û�ע��
        try:
            if not Search_Dao.search1('Students','StudentID',user_id):
                return False,"��ID�޽�ʦ��"
            elif not Security_tools.is_password_strong(password):
                return False,"����ǿ��������������������"
            else:
                Register_Dao.register_teacher(user_id,password)
                return True,"ע��ɹ�"
        except Exception as e:
            return False,"����ʧ��"
            return False



