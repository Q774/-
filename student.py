from db import create_connection, execute_read_query
import hashlib


class StudentSystem:
    def __init__(self):
        self.connection = create_connection()
        self.logged_in = False
        self.current_student = None

    def student_login(self, student_id, password):
        """学生登录"""
        if not self.connection:
            print("数据库连接失败")
            return False

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        query = "SELECT * FROM students WHERE student_id = %s AND password = %s"
        result = execute_read_query(self.connection, query, (student_id, hashed_password))

        if result:
            self.logged_in = True
            self.current_student = result[0]
            return True
        return False

    def view_my_violations(self):
        """查看自己的违纪记录"""
        if not self.logged_in:
            print("请先登录")
            return []

        query = """
        SELECT * FROM discipline_records 
        WHERE student_id = %s 
        ORDER BY violation_date DESC
        """
        return execute_read_query(self.connection, query,
                                  (self.current_student['student_id'],))

    def change_password(self, new_password):
        """修改密码"""
        if not self.logged_in:
            print("请先登录")
            return False

        hashed_password = hashlib.md5(new_password.encode()).hexdigest()
        query = """
        UPDATE students 
        SET password = %s 
        WHERE student_id = %s
        """
        return execute_query(self.connection, query,
                             (hashed_password, self.current_student['student_id']))

    def close_connection(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()