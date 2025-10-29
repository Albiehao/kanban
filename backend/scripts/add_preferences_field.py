#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""添加用户偏好设置字段"""

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
        print("正在添加偏好设置字段...")
        
        try:
            # 添加偏好设置字段
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN preferences TEXT NULL
            """)
            print("已添加 preferences 字段")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("preferences 字段已存在，跳过")
            else:
                raise
        
        connection.commit()
        print("\n数据库更新成功！")
        
except pymysql.Error as e:
    print(f"更新失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

