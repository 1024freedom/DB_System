from ctypes.wintypes import BOOL
from sqlite3 import Cursor
from utils.db_pool import DBPool
class Askpages_Dao:#分页查询
    def ask(base_sql:str,count_sql:str,page_size:int,current_page:int,ID:any):#预约记录查询
            try:
                conn = DBPool.get_instance().get_conn()
                cursor = conn.cursor()
            #获取总记录数
                cursor.execute(count_sql)
                total_records=cursor.fetchone()['total']
                #设置分页参数
                total_pages=(total_records+page_size-1)//page_size#向上取整
                #计算偏移量
                offset=(current_page-1)*page_size
                #分页查询
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