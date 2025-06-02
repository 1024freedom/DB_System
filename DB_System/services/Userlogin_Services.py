from sqlalchemy import true
from dao.Userlogin_Dao import Userlogin_Dao
from dao.Search_Dao import Search_Dao
from utils.Security_tools import Security_tools
class Userlogin_Services:
    @staticmethod
    def login(user_id,password):#�û���֤
        try:
            if not Search_Dao.search1('UserRoles','UserID',user_id):
                return False,"���û�����������������"
            user_password=Userlogin_Dao.get_user(user_id)['password']
            role=Userlogin_Dao.get_user(user_id)['Role']
            if Security_tools.verify_password(password,user_password):
                return True,"��֤�ɹ�",role
            else:
                return False,"�������"
        except Exception as e:
            return False,f"{str(e)}"





