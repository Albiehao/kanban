#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更新用户角色"""

import pymysql

# 数据库配置
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "todo_db"

try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    with connection.cursor() as cursor:
        # 备份现有用户
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_backup AS 
            SELECT * FROM users
        """)
        
        # 修改角色枚举类型
        cursor.execute("""
            ALTER TABLE users 
            MODIFY COLUMN role ENUM('user', 'admin', 'super_admin') 
            NOT NULL DEFAULT 'user'
        """)
        
        # 更新角色映射
        # student -> user
        cursor.execute("""
            UPDATE users SET role = 'user' WHERE role = 'student'
        """)
        
        # teacher -> user (保留数据)
        cursor.execute("""
            UPDATE users SET role = 'user' WHERE role = 'teacher'
        """)
        
        connection.commit()
        print("用户角色更新成功！")
        print("student/teacher -> user")
        
except pymysql.Error as e:
    print(f"更新失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

