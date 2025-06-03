from dao.Userlogin_Dao import Userlogin_Dao
from dao.Search_Dao import Search_Dao
from utils.Security_tools import Security_tools
class Userlogin_Services:
    @staticmethod
    def login(user_id,password):#用户认证
        try:
            if not Search_Dao.search1('UserRoles','UserID',user_id):
                return False,"该用户不存在请重新输入"
            user_password=Userlogin_Dao.get_user(user_id)['password']
            role=Userlogin_Dao.get_user(user_id)['Role']
            if Security_tools.verify_password(password,user_password):
                return True,"验证成功",role
            else:
                return False,"密码错误"
        except Exception as e:
            return False,f"{str(e)}"





