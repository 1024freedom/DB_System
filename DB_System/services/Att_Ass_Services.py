from sqlalchemy import true
from dao.Att_Ass_Dao import Att_Ass_Dao
from dao.Search_Dao import Search_Dao
from dao.Fetch_Dao import Fetch_Dao
import datetime
import re
from datetime import date
class Att_Ass_Services:
    @staticmethod
    def Attendance_add(StudentID,CourseID,Status):#���ڼ�¼
       try:
            if not Search_Dao.search1('Students','StudentID',StudentID):
                return False,"��ѧ�������ڣ�����������"
            if not Search_Dao.search2('Enrollments','CourseID','StudentID',CourseID,StudentID):
                return False,"�ÿγ̲����ڸ�ѧ���Ŀα��У����������룺"
            if Status not in ('����','�ٵ�','ȱ��'):
                return False,"״̬���Ϸ�������������"
            Date=date.today()
            Att_Ass_Dao.Attendance_add(StudentID,CourseID,Date,Status)
            return True,"�����ɹ�"
       except Exception as e:
            return False,f"{str(e)}"
    @staticmethod
    def Assignment_add(CourseID,Title,Deadline):#��ҵ����
        try:
            if not Search_Dao.search1('Courses','CourseID',CourseID):
                return False,"�ÿγ̲�����,����������"
            if not Title:
                return False,"���ⲻ��Ϊ��"
            #�������ʱ��
            pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"#ʱ���ʽ
            if not Deadline:
                return False,"��ֹʱ�䲻��Ϊ��"
            if not re.match(pattern,Deadline):
                return False,"��ʽ����,��ʹ��ʾ����ʽ"
            Att_Ass_Dao.Assignment_add(CourseID,Title,Deadline)
            return True,"�����ɹ�"
        except Exception as e:
            return False,f"{str(e)}"