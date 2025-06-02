from services.Students_Services import Students_Services
class Students_cli:
    @staticmethod
    def show_menu():
        print("\n===== 学生信息管理页面 =====")
        print("1. 单次增加学生信息")
        print("2. 更改学生联系方式")
        print("3. 为学生分配班级")
        print("4. 删除学生信息")
        print("5. 从excel文件导入学生信息")
        print("6. 导出学生信息为excel文件")
        print("0. 退出")
        print("========================")
    @staticmethod
    def add_student_once():#单次增加学生信息
        while True:
            while True:
                Name=input('输入姓名：').strip()
                if Name:
                    break
                print("姓名不能为空，请重新输入")
            while True:
                Gender=input('输入性别（男/女）：').strip()
                if Gender in ('男','女'):
                    break
                print ("请输入正确的性别：")
            while True:
                BirthDate=input('请输入正确的出生年月日（格式：YYYY-MM-DD').strip()
                if BirthDate:
                    break
                else:
                    print("不能为空，请重新输入")
            while True:
                Phone=input("请输入手机号：").strip()
                if not Phone:
                    Phone=None
                    break
                if len(Phone)!=11:
                    print("所输入手机号长度不合法，请重新输入")
                else:
                    break
            success,message=Students_Services.add_student_once(Name,Gender,BirthDate,Phone)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def alter_student_phone():#更改学生联系方式
        while True:
            while True:
                StudentID=input("请输入学生ID：").strip()
                if not StudentID:
                    print("学生ID不能为空，请重新输入")
                else:
                    break
            while True:
                Phone=input("请输入手机号：").strip()
                if len(Phone)!=11:
                    print("所输入手机号不合法，请重新输入")
                else:
                    break
            success,message=Students_Services.alter_student_phone(StudentID,Phone)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def alter_student_class():#为学生分配班级
        while True:
            while True:
                StudentID=input("请输入学生ID：").strip()
                if not StudentID:
                    print("学生ID不能为空，请重新输入")
                else:
                    break
            while True:
                ClassID=input("请输入要为该学生分配的班级号：")
                if not ClassID:
                    print("班级号不能为空，请重新输入")
                else:
                    break
            success,message=Students_Services.alter_student_class(StudentID,ClassID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def delete_student():  # 删除学生信息
        while True:
            while True:
                StudentID = input("请输入学生ID：").strip()
                if not StudentID:
                    print("学生ID不能为空，请重新输入")
                else:
                    break
            success,message=Students_Services.delete_student(StudentID)
            if success:
                print(message)
                break
            else:
                print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def import_from_excel():#从excel文件导入学生数据到数据库
        filepath=input("请输入文件的绝对路径")
        success,message=Students_Services.import_from_excel(filepath)
        if success:
            print(message)
        else:
            print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def export_to_excel():#以excel文件形式批量导出学生信息
        filepath=input("请输入导出路径")
        success,message=Students_Services.export_to_excel(filepath)
        if success:
            print(message)
        else:
            print('\033[91m' + message + '\033[0m')#红色文本
    @staticmethod
    def run():
        Students_cli.show_menu()
        choice=1
        while choice:
            choice=input("请选择操作：").strip()
            match choice:
                case 1:
                    Students_cli.add_student_once()
                case 2:
                    Students_cli.alter_student_phone()
                case 3:
                    Students_cli.alter_student_class()
                case 4:
                    Students_cli.delete_student()
                case 5:
                    Students_cli.import_from_excel()
                case 6:
                    Students_cli.export_to_excel()
               