from ctypes.wintypes import BOOL
from sqlite3 import Cursor
from numpy._core.multiarray import normalize_axis_index
from pymysql import NULL
from sqlalchemy import Boolean
from utils.db_pool import DBPool
class Askpages_Dao:#��ҳ��ѯ
    def ask(base_sql:str,count_sql:str,page_size:int,current_page:int,ID:any):#ԤԼ��¼��ѯ
            try:
                conn = DBPool.get_instance().get_conn()
                cursor = conn.cursor()
            #��ȡ�ܼ�¼��
                cursor.execute(count_sql)
                total_records=cursor.fetchone()['total']
                #���÷�ҳ����
                total_pages=(total_records+page_size-1)//page_size#����ȡ��
                #����ƫ����
                offset=(current_page-1)*page_size
                #��ҳ��ѯ
                if ID:
                    base_sql=base_sql(ID,page_size,offset)
                    cursor.execute(base_sql,(ID,page_size,offset))
                    reservations=cursor.fetchall()
                else:
                    base_sql=base_sql(page_size,offset)
                    cursor.execute(base_sql,(page_size,offset))
                    reservations=cursor.fetchall()
                return {
                    'data':reservations,
                    'total_pages':total_pages,
                    'total_records':total_records
                    }
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()