from sqlite3 import Cursor
from utils.db_pool import DBPool
from datetime import datetime
class Reservations_Dao:
    @staticmethod
    def lab_reservation(TeacherID,LabID,StartTime,EndTime):#实验室预约
        conn = DBPool.get_instance().get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Labreserations (TeacherID,LabID,StartTime,EndTime) VALUES (%s,%s,%s,%s)",(TeacherID,LabID,StartTime,EndTime,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    @staticmethod
    def reservation_cancel(TeacherID,ReservationID):#取消未开始的预约
            conn = DBPool.get_instance().get_conn()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM LabReservations WHERE TeacherID=%s AND ReservationID=%s",(TeacherID,ReservationID,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()