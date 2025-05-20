import pymysql
from dbutils.pooled_db import PooledDB
class DBPool:
    _instance=None#单例模式
    def __init__(self):
        self.pool=PooledDB(
            creator=pymysql,#指定数据库驱动
            maxconnections=100,#连接池允许的最大连接数
            mincached=10,#初始化时连接池至少创建的空闲连接数
            host='localhost',
            user='root',
            password='20050119Sh?',
            database='education_system',
            )
        @classmethod
        def get_instance(cls):
            if not cls._instance:
                cls._instance=cls()#初始化实例
                return cls._instance

        def get_conn(self):
            return self.pool.connection()#从连接池获取一个可用的数据库对象