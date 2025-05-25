import pymysql
from dbutils.pooled_db import PooledDB
class DBPool:
    _instance=None#����ģʽ,ȷ��һ����ֻ��һ��ʵ�����ṩȫ�ַ��ʵ�
    def __init__(self):
        self.pool=PooledDB(
            creator=pymysql,#ָ�����ݿ�����
            maxconnections=100,#���ӳ���������������
            mincached=10,#��ʼ��ʱ���ӳ����ٴ����Ŀ���������
            host='localhost',
            user='root',
            password='20050119Sh?',
            database='education_system',
            )
        @classmethod
        def get_instance(cls):#������
            if not cls._instance:
                cls._instance=cls()#��ʼ��ʵ��
                return cls._instance
        #get_instance����ȷ���������ӳ���ȫ�ַ�Χ����Ψһ��
        def get_conn(self):
            return self.pool.connection()#�����ӳػ�ȡһ�����õ����ݿ����