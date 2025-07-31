from db import create_connection, execute_query, execute_read_query
import hashlib


class AdminSystem:
    def __init__(self):
        self.connection = create_connection()
        self.logged_in = False
        self.current_admin = None

    def admin_login(self, username, password):
        """管理员登录"""
        if not self.connection:
            print("数据库连接失败")
            return False

        # 密码加密
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        query = "SELECT * FROM admins WHERE username = %s AND password = %s"
        result = execute_read_query(self.connection, query, (username, hashed_password))

        if result:
            self.logged_in = True
            self.current_admin = result[0]
            print("登录成功！")
            return True
        print("用户名或密码错误")
        return False

    def add_student(self, student_id, name, class_, password='123456'):
        """添加学生"""
        if not self.logged_in:
            print("请先登录")
            return False

        # 密码加密
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        query = """
        INSERT INTO students (student_id, name, class, password) 
        VALUES (%s, %s, %s, %s)
        """
        return execute_query(self.connection, query,
                             (student_id, name, class_, hashed_password))

    def add_violation(self, student_id, violation_type, violation_date,
                      description, punishment):
        """添加违纪记录"""
        if not self.logged_in:
            print("请先登录")
            return False

        query = """
        INSERT INTO discipline_records 
        (student_id, violation_type, violation_date, description, punishment, handler) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        return execute_query(self.connection, query,
                             (student_id, violation_type, violation_date,
                              description, punishment, self.current_admin['username']))

    def query_students(self, keyword=None):
        """查询学生"""
        if not self.logged_in:
            print("请先登录")
            return []

        query = "SELECT student_id, name, class FROM students"
        params = []
        if keyword:
            query += " WHERE student_id LIKE %s OR name LIKE %s OR class LIKE %s"
            params = [f'%{keyword}%'] * 3

        return execute_read_query(self.connection, query, params)

    def query_violations(self, student_id=None, start_date=None, end_date=None):
        """查询违纪记录"""
        if not self.logged_in:
            print("请先登录")
            return []

        query = """
        SELECT r.*, s.name, s.class FROM discipline_records r
        JOIN students s ON r.student_id = s.student_id
        WHERE 1=1
        """
        params = []

        if student_id:
            query += " AND r.student_id = %s"
            params.append(student_id)
        if start_date:
            query += " AND r.violation_date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND r.violation_date <= %s"
            params.append(end_date)

        return execute_read_query(self.connection, query, params)

    def get_violation_stats(self):
        """获取违纪统计数据"""
        if not self.logged_in:
            print("请先登录")
            return []

        query = """
        SELECT violation_type, COUNT(*) as count 
        FROM discipline_records 
        GROUP BY violation_type 
        ORDER BY count DESC
        """
        return execute_read_query(self.connection, query)

    def close_connection(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()