from dao.Enrollments_Dao import Enrollments_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
class Enrollments_Servises:
    @staticmethod
    def students_enroll():#ѧ��ѡ��

    @staticmethod
    def students_drop_course():#ѧ���˿�
        while True:
            StudentID=input("������ѧ��").strip()
            if StudentID:
                if not Search_Dao.search1('Enrollments','StudentID',StudentID):
                    print("ѡ�μ�¼�в����ڸ�ѧ�ţ�����������")
                else:
                    break
            else:
                print("ѧ�Ų���Ϊ�գ�����������")
        while True:
            CourseID=input("������Ҫ��ѡ�Ŀγ�ID").strip()
            if CourseID:
                if not Search_Dao.search2('Enrollments','StudentID','CourseID',StudentID,CourseID):
                    print("ѡ�μ�¼�в����ڸÿγ̣�����������")
                else:
                    break
            else:
                print("�γ̺Ų���Ϊ�գ�����������")
        try:
            Enrollments_Dao.students_drop_course(StudentID,CourseID)
            return True,"�����ɹ�"
        except Exception as e:
            print(f"����ʧ�ܣ�{str(e)}")



