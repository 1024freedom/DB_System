from dao.Permissions_Dao import Permissions_Dao
import json
class Permissions_Services:
    @staticmethod
    def get_user_role(user_id):#获取用户角色
        return Permissions_Dao.get_user_role(user_id)
    @staticmethod
    def get_user_permissions(user_id):#获取用户完整权限信息
        result = Permissions_Dao.get_user_permissions(user_id)
        if not result:
            return None
        
        # 合并默认权限和用户特定权限
        merged_permissions = {}
        
        # 递归合并权限字典
        def merge_dicts(default, custom):
            for key, value in custom.items():
                if key in default:
                    if isinstance(value, dict) and isinstance(default[key], dict):
                        merge_dicts(default[key], value)
                    else:
                        default[key] = value
                else:
                    default[key] = value
            
        # 复制默认权限作为基础
        if result['default_permissions']:
            merged_permissions = json.loads(json.dumps(result['default_permissions']))
        
        # 合并用户特定权限
        if result['permisssions']:
            merge_dicts(merged_permissions, result['permisssions'])
        
        return {
            'user_id': user_id,
            'role': result['role'],
            'permissions': merged_permissions,
            'default_permissions': result['default_permissions'],
            'custom_permissions': result['permisssions']
        }
    @staticmethod
    def update_user_permissions(user_id, permissions):#更新用户权限
        return Permissions_Dao.update_user_permissions(user_id, permissions)
    @staticmethod
    def modify_permission(user_id, permission_path, value):#修改用户特定权限
        return Permissions_Dao.modify_permission(user_id, permission_path, value)
    @staticmethod
    def grant_permission(user_id, permission_path):#授予权限
        return Permissions_Dao.grant_permission(user_id, permission_path)
    @staticmethod
    def revoke_permission(user_id, permission_path):#撤销权限
        return Permissions_Dao.revoke_permission(user_id, permission_path)
    @staticmethod
    def get_role_default_permissions(role):#获取角色默认权限
        return Permissions_Dao.get_role_default_permission(role)
    @staticmethod
    def set_role_default_permissions(role, permissions):#设置角色默认权限
        return Permissions_Dao.set_role_default_permissions(role, permissions)
    @staticmethod
    def update_permission_tree():#更新权限树
        return Permissions_Dao.update_permission_tree()





