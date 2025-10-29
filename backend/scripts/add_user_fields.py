#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""添加用户个人介绍和头像字段"""

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
        print("正在更新用户表结构...")
        
        # 检查字段是否已存在并添加
        try:
            # 添加个人介绍字段
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN bio VARCHAR(500) NULL
            """)
            print("已添加 bio 字段")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("bio 字段已存在，跳过")
            else:
                raise
        
        try:
            # 添加头像URL字段
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN avatar_url VARCHAR(255) NULL
            """)
            print("已添加 avatar_url 字段")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("avatar_url 字段已存在，跳过")
            else:
                raise
        
        connection.commit()
        print("\n数据库更新成功！")
        
except pymysql.Error as e:
    print(f"更新失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

