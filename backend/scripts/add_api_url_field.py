#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""添加api_url字段到edu_account_bindings表"""

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
        # 检查是否存在 api_url 列
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'edu_account_bindings' AND COLUMN_NAME = 'api_url'
        """, (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            print("添加新字段: api_url...")
            cursor.execute("""
                ALTER TABLE edu_account_bindings 
                ADD COLUMN api_url VARCHAR(255) DEFAULT 'http://160.202.229.142:8000/api/v1/api/courses' 
                AFTER api_key
            """)
            connection.commit()
            print("[成功] 字段添加完成！")
        else:
            print("[信息] api_url 字段已存在")
        
except pymysql.Error as e:
    print(f"[失败] 添加字段失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

