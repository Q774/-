import mysql.connector


def create_connection():
    """创建数据库连接"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='disciplinary_system',
            user='root',       # 替换为你的MySQL用户名
            password='qq822615.'  # 替换为你的MySQL密码
        )
        if connection.is_connected():
            return connection
    except mysql as e:
        print(f"数据库连接错误: {e}")
    return connection

def execute_query(connection, query, params=None):
    """执行INSERT/UPDATE/DELETE语句"""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return True
    except mysql as e:
        print(f"执行查询错误: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def execute_read_query(connection, query, params=None):
    """执行SELECT语句"""
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql as e:
        print(f"查询错误: {e}")
        return None
    finally:
        cursor.close()
        var = mysql.connector
import mysql.connector

def create_connection():
    """创建数据库连接"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='disciplinary_system',
            user='root',       # 替换为你的MySQL用户名
            password='123456'  # 替换为你的MySQL密码
        )
        if connection.is_connected():
            return connection
    except mysql as e:
        print(f"数据库连接错误: {e}")
    return connection

def execute_query(connection, query, params=None):
    """执行INSERT/UPDATE/DELETE语句"""
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return True
    except mysql as e:
        print(f"执行查询错误: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def execute_read_query(connection, query, params=None):
    """执行SELECT语句"""
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql as e:
        print(f"查询错误: {e}")
        return None
    finally:
        cursor.close()