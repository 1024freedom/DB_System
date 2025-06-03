from sqlite3 import Cursor
from utils.db_pool import DBPool
class Userlogin_Dao:
    @staticmethod
    def get_user(user_id):#获取用户认证信息
        conn=DBPool.get_instance().get_conn()
        cursor=conn.cursor()
        try:
            sql = """
            SELECT Role, Password 
            FROM  UserRoles
            WHERE UserID = %s
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()





