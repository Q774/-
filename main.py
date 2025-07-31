from admin import AdminSystem
from student import StudentSystem
import datetime


def admin_menu(admin_sys):
    """管理员菜单"""
    while True:
        print("\n===== 管理员后台 =====")
        print("1. 添加学生")
        print("2. 录入违纪记录")
        print("3. 查询学生")
        print("4. 查询违纪记录")
        print("5. 违纪统计分析")
        print("6. 退出登录")

        choice = input("请选择功能: ")

        if choice == '1':
            student_id = input("请输入学号: ")
            name = input("请输入姓名: ")
            class_ = input("请输入班级: ")
            if admin_sys.add_student(student_id, name, class_):
                print("添加成功")
            else:
                print("添加失败")

        elif choice == '2':
            student_id = input("请输入学号: ")
            violation_type = input("请输入违纪类型: ")
            violation_date = input("请输入违纪日期(YYYY-MM-DD): ")
            description = input("请输入违纪描述: ")
            punishment = input("请输入处分结果: ")

            try:
                # 验证日期格式
                datetime.datetime.strptime(violation_date, '%Y-%m-%d')
                if admin_sys.add_violation(student_id, violation_type,
                                           violation_date, description, punishment):
                    print("录入成功")
                else:
                    print("录入失败")
            except ValueError:
                print("日期格式错误，请使用YYYY-MM-DD格式")

        elif choice == '3':
            keyword = input("请输入查询关键词(学号/姓名/班级，为空则查询全部): ")
            students = admin_sys.query_students(keyword)
            if students:
                print("\n查询结果:")
                print(f"{'学号':<15} {'姓名':<10} {'班级'}")
                print("-" * 40)
                for s in students:
                    print(f"{s['student_id']:<15} {s['name']:<10} {s['class']}")
            else:
                print("没有找到相关学生")

        elif choice == '4':
            student_id = input("请输入学号(为空则查询全部): ")
            start_date = input("请输入开始日期(YYYY-MM-DD，为空则不限制): ")
            end_date = input("请输入结束日期(YYYY-MM-DD，为空则不限制): ")

            violations = admin_sys.query_violations(student_id, start_date, end_date)
            if violations:
                print("\n查询结果:")
                print(f"{'学号':<15} {'姓名':<10} {'班级':<10} {'违纪类型':<15} {'日期':<12} {'处分结果'}")
                print("-" * 80)
                for v in violations:
                    print(f"{v['student_id']:<15} {v['name']:<10} {v['class']:<10} "
                          f"{v['violation_type']:<15} {v['violation_date']:<12} {v['punishment']}")
            else:
                print("没有找到相关违纪记录")

        elif choice == '5':
            stats = admin_sys.get_violation_stats()
            if stats:
                print("\n违纪类型统计:")
                print(f"{'违纪类型':<20} {'次数'}")
                print("-" * 30)
                for s in stats:
                    print(f"{s['violation_type']:<20} {s['count']}")
            else:
                print("没有违纪记录数据")

        elif choice == '6':
            print("退出登录成功")
            break

        else:
            print("无效的选择，请重新输入")


def student_menu(student_sys):
    """学生菜单"""
    while True:
        print("\n===== 学生前台 =====")
        print(f"当前登录: {student_sys.current_student['name']} "
              f"({student_sys.current_student['student_id']})")
        print("1. 查看我的违纪记录")
        print("2. 修改密码")
        print("3. 退出登录")

        choice = input("请选择功能: ")

        if choice == '1':
            violations = student_sys.view_my_violations()
            if violations:
                print("\n您的违纪记录:")
                print(f"{'违纪类型':<15} {'日期':<12} {'描述':<30} {'处分结果'}")
                print("-" * 70)
                for v in violations:
                    print(f"{v['violation_type']:<15} {v['violation_d']:<12}"
                          f" {v['description'][:25]}...<30 {v['punish']}")
            else:
                print("您没有违纪记录")

        elif choice == '2':
            new_pwd = input("请输入新密码: ")
            confirm_pwd = input("请确认新密码: ")
            if new_pwd == confirm_pwd:
                if student_sys.change_password(new_pwd):
                    print("密码修改成功，请重新登录")
                    break
                else:
                    print("密码修改失败")
            else:
                print("两次输入的密码不一致")

        elif choice == '3':
            print("退出登录成功")
            break

        else:
            print("无效的选择，请重新输入")


def main():
    """主函数"""
    while True:
        print("\n===== 违纪学生管理系统 =====")
        print("1. 管理员登录")
        print("2. 学生登录")
        print("3. 退出系统")

        choice = input("请选择登录身份: ")

        if choice == '1':
            admin_sys = AdminSystem()
            username = input("请输入管理员用户名: ")
            password = input("请输入管理员密码: ")

            if admin_sys.admin_login(username, password):
                admin_menu(admin_sys)
            else:
                print("管理员登录失败")

            admin_sys.close_connection()

        elif choice == '2':
            student_sys = StudentSystem()
            student_id = input("请输入学号: ")
            password = input("请输入密码: ")

            if student_sys.student_login(student_id, password):
                student_menu(student_sys)
            else:
                print("学生登录失败")

            student_sys.close_connection()

        elif choice == '3':
            print("感谢使用，再见！")
            break

        else:
            print("无效的选择，请重新输入")


if __name__ == "__main__":
    main()
