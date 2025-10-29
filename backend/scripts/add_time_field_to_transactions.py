#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""为transactions表添加time字段"""

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
        print("正在检查transactions表结构...")
        
        # 检查time字段是否已存在
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'transactions' 
            AND COLUMN_NAME = 'time'
        """, (DB_NAME,))
        
        if cursor.fetchone():
            print("time字段已存在，跳过添加")
        else:
            print("正在添加time字段...")
            cursor.execute("""
                ALTER TABLE transactions 
                ADD COLUMN time TIME NULL COMMENT '具体时间，格式：HH:MM:SS，可选'
                AFTER date
            """)
            connection.commit()
            print("time字段添加成功！")
        
except pymysql.Error as e:
    print(f"操作失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

