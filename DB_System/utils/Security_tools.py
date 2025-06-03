import bcrypt
import secrets
class Security_tools:
    @staticmethod
    def hash_password(password):#哈希密码
        salt=bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'),salt).decode('utf-8')
    @staticmethod
    def verify_password(password,hashed_password):#验证密码
        return bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))
    @staticmethod
    def is_password_strong(password):#验证密码强度
        if len(password)<8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        return True

