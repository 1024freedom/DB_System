from dao.Permissions_Dao import Permissions_Dao
import json
class Permissions_Services:
    @staticmethod
    def get_user_role(user_id):#��ȡ�û���ɫ
        return Permissions_Dao.get_user_role(user_id)
    @staticmethod
    def get_user_permissions(user_id):#��ȡ�û�����Ȩ����Ϣ
        result = Permissions_Dao.get_user_permissions(user_id)
        if not result:
            return None
        
        # �ϲ�Ĭ��Ȩ�޺��û��ض�Ȩ��
        merged_permissions = {}
        
        # �ݹ�ϲ�Ȩ���ֵ�
        def merge_dicts(default, custom):
            for key, value in custom.items():
                if key in default:
                    if isinstance(value, dict) and isinstance(default[key], dict):
                        merge_dicts(default[key], value)
                    else:
                        default[key] = value
                else:
                    default[key] = value
            
        # ����Ĭ��Ȩ����Ϊ����
        if result['default_permissions']:
            merged_permissions = json.loads(json.dumps(result['default_permissions']))
        
        # �ϲ��û��ض�Ȩ��
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
    def update_user_permissions(user_id, permissions):#�����û�Ȩ��
        return Permissions_Dao.update_user_permissions(user_id, permissions)
    @staticmethod
    def modify_permission(user_id, permission_path, value):#�޸��û��ض�Ȩ��
        return Permissions_Dao.modify_permission(user_id, permission_path, value)
    @staticmethod
    def grant_permission(user_id, permission_path):#����Ȩ��
        return Permissions_Dao.grant_permission(user_id, permission_path)
    @staticmethod
    def revoke_permission(user_id, permission_path):#����Ȩ��
        return Permissions_Dao.revoke_permission(user_id, permission_path)
    @staticmethod
    def get_role_default_permissions(role):#��ȡ��ɫĬ��Ȩ��
        return Permissions_Dao.get_role_default_permission(role)
    @staticmethod
    def set_role_default_permissions(role, permissions):#���ý�ɫĬ��Ȩ��
        return Permissions_Dao.set_role_default_permissions(role, permissions)
    @staticmethod
    def update_permission_tree():#����Ȩ����
        return Permissions_Dao.update_permission_tree()





