from sqlite3 import Cursor
import stat
from openpyxl import Workbook
from utils.db_pool import DBPool
from sqlalchemy import create_engine
import pandas as pd
import json
import datetime
class Permissions_Dao:
    @staticmethod
    def get_user_role(user_id):#获取用户角色
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Role FROM UserRoles WHERE UserID=%s",(user_id,))
            result=cursor.fetchone()
            return result['Role'] if result else None
        except Exception as e:
            return None
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def get_user_permissions(user_id):#获取用户权限（包含角色默认权限和用户特定权限）
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT ur.Role, ur.Permissions AS UserPermissions, rd.DefaultPermissions
            FROM UserRoles ur
            LEFT JOIN RoleDefaults rd ON ur.Role = rd.Role
            WHERE ur.UserID = %s
            """,(user_id,))
            result=cursor.fetchone()
            if result:
                #解析json数据
                user_perms=json.loads(result['UserPermissions']) if result['UserPermissions'] else {}
                default_perms=json.loads(result['DefaultPermissions']) if result['DefaultPermissions'] else {}
                return{
                    'role':result['role'],
                    'permisssions':user_perms,
                    'default_permissions':default_perms
                    
                    }
            return None
        except Exception as e:
            return None
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def update_user_permissions(user_id,permissions):#更新用户权限
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            perm_json=json.dumps(permissions)
            cursor.execute("""
            UPDATE UserRoles
            SET Permissions = %s
            WHERE UserID = %s
            """,(user_id,))
            conn.commit()
            return True,"操作成功"
        except Exception as e:
            conn.rollback()
            raise e
            return False
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def modify_permission(user_id,permission_path,value):#修改特定权限
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            sql=f"""
            UPDATE UserRoles
            SET Permissions = JSON_SET(
                COALESCE(Permissions, '{{}}'),
                '$.{permission_path.replace('.', '".')}', %s
            )
            WHERE UserID = %s
            """#更新特定路径
            cursor.execute(sql,(value,user_id,))
            conn.commit()
            return True,"操作成功"
        except Exception as e:
            conn.rollback()
            raise e
            return False
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def grant_permission(user_id,permission_path):#授予特定权限
        return Permissions_Dao.modify_permission(user_id,permission_path,True)
    @staticmethod
    def revoke_permission(user_id,permission_path):#撤销特定权限
        return Permissions_Dao.modify_permission(user_id,permission_path,False)
    @staticmethod
    def get_role_default_permission(role):#获取角色默认权限
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT DefaultPermissions FROM RoleDefaults WHERE Role=%s",(role,))
            result=cursor.fetchone()
            return json.loads(result['DefaultPermissions']) if result else None
        except Exception as e:
            raise e
            return None
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def set_role_default_permissions(role,permissions):#设置角色默认权限
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            perms_json=json.dumps(permissions)
            sql="""
            INSERT INTO RoleDefaults (Role, DefaultPermissions)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE DefaultPermissions = VALUES(DefaultPermissions)
            """#插入新角色+权限或更新已有角色权限
            cursor.execute(sql,(role,perms_json,))
            conn.commit()
            return True,"操作成功"
        except Exception as e:
            conn.rollback()
            raise e
            return False
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def collect_permission_paths(permission_dict,current_path,path_set):#递归收集权限路径
        if not permission_dict:
            return
        for key,value in permission_dict.items():
            new_path=f"{current_path}.{key}" if current_path else key
            if isinstance(value,bool):#如果是布尔值，表明这是一个节点
                path_set.add(new_path)
            elif isinstance(value,dict):#如果是字典，递归
                Permissions_Dao.collect_permission_paths(value,new_path,path_set)
    @staticmethod
    def update_permission_tree():#根据用户权限和角色默认权限更新权限树
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            #收集所有实际使用的权限路径
            all_permissions=set()
            #从用户权限表收集权限路径
            cursor.execute("SELECT Permissions FROM UserRoles WHERE Permissions IS NOT NULL")
            user_perms=cursor.fetchall()
            for row in user_perms:
                if row['Permission']:
                    perms_dict=json.loads(row['Permissions'])
                    Permissions_Dao.collect_permission_paths(perms_dict,"",all_permissions)
            #从角色默认权限表收集权限路径
            cursor.execute("SELECT Permissions FROM UserRoles WHERE Permissions IS NOT NULL")
            user_perms=cursor.fetchall()
            for row in user_perms:
                if row['Permission']:
                    perms_dict=json.loads(row['Permissions'])
                    Permissions_Dao.collect_permission_paths(perms_dict,"",all_permissions)
            #获取现有权限树中的权限ID(ID即为路径)
            cursor.execute("SELECT PermissionID FROM PermissionTree")
            existing_perms={row['PermissionID'] for row in cursor.fetchall()}
            #添加缺失的权限节点
            for perm_path in all_permissions:
                if perm_path not in existing_perms:
                    #解析路径
                    parts=perm_path.split('.')
                    name=parts[-1].capitalize().replace('_',' ')
                    #确定父节点
                    parent_id=None
                    if len(parts)>1:
                        parent_id='.'.join(parts[:-1])

                    #确定节点类型
                    node_type="action"#默认为操作节点
                    if len(parts)==1:
                        node_type="module"
                    elif len(parts)==2:
                        node_type="page"
                    sql="""
                        INSERT INTO PermissionTree (PermissionID, ParentID, Name, Type)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            ParentID = VALUES(ParentID),
                            Name = VALUES(Name),
                            Type = VALUES(Type)
                    """
                    cursor.execute(sql,(perm_path,parent_id,name,node_type))
            conn.commit()
            return True,"更新权限树成功"
        except Exception as e:
            conn.rollback()
            raise e
            return False
        finally:
            cursor.close()
            conn.close()
    
