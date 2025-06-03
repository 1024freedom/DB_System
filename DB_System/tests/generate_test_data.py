from sqlite3 import Cursor
import sys
import os
from pathlib import Path
# 解决导入问题：将项目根目录添加到 Python 路径
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent  # 获取项目根目录 (DB_System)
sys.path.append(str(project_root))
from utils.db_pool import DBPool
from faker import Faker
import random
import datetime
from datetime import time
from tqdm import tqdm#显示进度条


fake=Faker('zh_CN')#使用中文数据
conn = DBPool.get_instance().get_conn()
cursor = conn.cursor()

def generate_teachers(num):#生成教师数据
    titles=['教授','副教授','院长','副院长','讲师','助教','特聘教授']
    for _ in tqdm(range(num),desc="生成教师数据"):
        name=fake.name()
        title=random.choice(titles)
        cursor.execute("INSERT INTO Teachers(Name,Title) VALUES(%s,%s)",(name,title,))
        conn.commit()
    print(f"已插入{num}条教师数据")
def generate_classes(num):#生成班级数据
    majors=['软件工程','计算机科学与技术','人工智能','网络工程','网络安全','电子信息','大数据科学与技术','密码科学与技术','数学与计算科学','生物工程','临床医学','航空航天工程','飞行器设计','能源与动力工程','机械工程']
    for _ in tqdm(range(num),desc="生成班级数据"):
        class_name=f"{fake.random_element(['软件','计算机','网络','大数据','密码','数学','生物','医学','航空航天','能源','机械'])}"\
                    f"{random.randint(1, 10)}" \
                    f"{fake.random_element(['班'])}"
        major=random.choice(majors)
        cursor.execute("INSERT INTO Classes (ClassName,Major) VALUES (%s,%s)",(class_name,major,))
        conn.commit()
    print(f"已插入{num}条班级数据")
def generate_students(num):#生成学生数据
    # 获取所有班级ID
    cursor.execute("SELECT ClassID FROM Classes")
    class_ids = [row[0] for row in cursor.fetchall()]
    
    # 用于记录每个班级的学生数量
    class_counts = {cid: 0 for cid in class_ids}
    
    for _ in tqdm(range(num), desc="生成学生数据"):
        name = fake.name()
        gender = random.choice(['男', '女'])
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=25)
        phone = fake.phone_number()
        class_id = random.choice(class_ids)
        
        # 确保学生数量不超过班级容量
        cursor.execute("SELECT Capacity, CapacityNow FROM Classes WHERE ClassID = %s", (class_id,))
        capacity, capacity_now = cursor.fetchone()
        
        if capacity_now >= capacity:
            # 如果班级已满，随机分配到其他班级
            class_id = random.choice([cid for cid in class_ids if class_counts[cid] < capacity])
        
        cursor.execute(
            "INSERT INTO Students (Name, Gender, BirthDate, Phone, ClassID) VALUES (%s, %s, %s, %s, %s)",
            (name, gender, birth_date, phone, class_id,)
        )
        
        # 更新班级当前人数
        class_counts[class_id] += 1
        cursor.execute(
            "UPDATE Classes SET CapacityNow = CapacityNow + 1 WHERE ClassID = %s",
            (class_id,)
        )
    
    conn.commit()
    print(f"已插入 {num} 条学生数据")

def generate_courses(num):#生成课程数据
    # 获取所有教师ID
    cursor.execute("SELECT TeacherID FROM Teachers")
    teacher_ids = [row[0] for row in cursor.fetchall()]
    
    course_names = [
        '高等数学', '线性代数', '概率论', '离散数学', '数据结构', 
        '算法分析', '操作系统', '计算机网络', '数据库系统原理', '软件工程',
        '人工智能导论', '机器学习', '深度学习', '计算机视觉', '自然语言处理',
        'Java程序设计', 'Python编程', 'C++程序设计', 'Web前端开发', '移动应用开发'
    ]
    
    # 课程时间段
    time_slots = [
        (time(8, 0), time(9, 40)),
        (time(10, 0), time(11, 40)),
        (time(14, 0), time(15, 40)),
        (time(16, 0), time(17, 40)),
        (time(19, 0), time(20, 40))
    ]
    
    for _ in tqdm(range(num), desc="生成课程数据"):
        course_name = f"{random.choice(course_names)}{random.choice(['基础', '进阶', '实践', '理论'])}"
        credit = random.randint(1, 5)
        teacher_id = random.choice(teacher_ids) if teacher_ids else None
        capacity = random.randint(100, 200)
        day = random.randint(1, 7)
        start_time, end_time = random.choice(time_slots)
        
        cursor.execute(
            "INSERT INTO Courses (CourseName, Credit, TeacherID, Capacity, Day, StartTime, EndTime) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (course_name, credit, teacher_id, capacity, day, start_time, end_time,)
        )
    
    conn.commit()
    print(f"已插入 {num} 条课程数据")

def generate_classrooms(num):#生成教室数据
    building_names = ['一号教学楼', '二号教学楼', '三号教学楼', '软件学院', '计算机与信息工程学院', '曾宪梓楼']
    room_types = ['普通教室', '实验室']
    
    for i in tqdm(range(num), desc="生成教室数据"):
        building = random.choice(building_names)
        floor = random.randint(1, 6)
        room_number = f"{floor}{random.randint(1, 30):02d}"
        location = f"{building}{room_number}"
        room_type = random.choice(room_types)
        
        # 不同类型教室的容量不同
        if room_type == '普通教室':
            capacity = random.randint(50, 200)
        else:  # 实验室
            capacity = random.randint(20, 50)
        cursor.execute(
            "INSERT INTO Classrooms (Location, Type,Capacity) VALUES (%s, %s,%s)",
            (location, room_type,capacity)
        )
    
    conn.commit()
    print(f"已插入 {num} 条教室数据")

def generate_textbooks(num):#生成教材数据
    # 获取所有课程ID
    cursor.execute("SELECT CourseID FROM Courses")
    course_ids = [row[0] for row in cursor.fetchall()]
    
    subjects = ['数学', '物理', '化学', '生物医学', '计算机', 'C语言程序设计', 
                '算法', '网络', '数据库系统原理', '人工智能', '机器学习', '软件工程']
    
    for _ in tqdm(range(num), desc="生成教材数据"):
        subject = random.choice(subjects)
        title = f"{subject}{random.choice(['导论', '基础', '原理', '实践', '进阶'])}"
        author = fake.name()
        publisher = random.choice(['高等教育出版社', '清华大学出版社', '人民邮电出版社', '机械工业出版社'])
        course_id = random.choice(course_ids) if course_ids else None
        
        cursor.execute(
            "INSERT INTO Textbooks (Title, Author, Publisher, CourseID) VALUES (%s, %s, %s, %s)",
            (title, author, publisher, course_id)
        )
    
    conn.commit()
    print(f"已插入 {num} 条教材数据")

def generate_books(num):#生成图书数据
    categories = ['小说', '文学', '历史', '哲学', '科学', '技术', '艺术', '教育', '经济', '管理']
    
    for _ in tqdm(range(num), desc="生成图书数据"):
        category = random.choice(categories)
        book_name = f"{category}{random.choice(['导论', '基础', '原理', '实践', '进阶'])}"
        author = fake.name()
        publisher = random.choice(['人民文学出版社', '商务印书馆', '三联书店', '中华书局', '中华出版社'])
        reserve = random.randint(1, 50)
        
        cursor.execute(
            "INSERT INTO Books (BookName, Author, Publisher, Reserve) VALUES (%s, %s, %s, %s)",
            (book_name, author, publisher, reserve)
        )
    
    conn.commit()
    print(f"已插入 {num} 条图书数据")

def generate_equipment(num):#生成设备数据
    equipment_types = ['投影仪', '显微镜', '示波器', '打印机', 
                      '服务器', '路由器', '交换机', '实验台', '传感器']
    
    for _ in tqdm(range(num), desc="生成设备数据"):
        equipment_name = f"{random.choice(equipment_types)}{random.choice(['', '（高级）', '（专业级）'])}"
        reserve = random.randint(1, 50)
        
        cursor.execute(
            "INSERT INTO Equipments (EquipmentName, Reserve) VALUES (%s, %s)",
            (equipment_name, reserve)
        )
    
    conn.commit()
    print(f"已插入 {num} 条设备数据")

def main():
    try:
        generate_teachers(300)        # 教师表
        generate_classes(300)         # 班级表
        generate_students(10000)     # 学生表
        generate_courses(100)        # 课程表
        generate_classrooms(500)      # 教室表
        generate_textbooks(2000)      # 教材表
        generate_books(500)          # 图书表
        generate_equipment(300)      # 设备表
        
        print("所有测试数据生成完成！")
        
    except Exception as e:
        print('\033[91m' + str(e)+ '\033[0m')#红色文本
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("教务系统数据库基础数据批量生成：")
    print("=" * 50)
    main()



