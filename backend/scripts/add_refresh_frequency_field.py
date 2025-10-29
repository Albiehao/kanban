#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""添加刷新频率字段到教务系统绑定表"""

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
        print("正在检查 refresh_frequency 字段...")
        
        # 检查字段是否存在
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'edu_account_bindings' 
            AND COLUMN_NAME = 'refresh_frequency'
        """, (DB_NAME,))
        
        exists = cursor.fetchone()
        
        if not exists:
            print("添加 refresh_frequency 字段...")
            cursor.execute("""
                ALTER TABLE edu_account_bindings 
                ADD COLUMN refresh_frequency VARCHAR(10) DEFAULT '1.0' 
                COMMENT '刷新频率（小时）' 
                AFTER edu_password
            """)
            connection.commit()
            print("refresh_frequency 字段添加成功！")
            
            # 为现有记录设置默认值
            cursor.execute("""
                UPDATE edu_account_bindings 
                SET refresh_frequency = '1.0' 
                WHERE refresh_frequency IS NULL
            """)
            connection.commit()
            print("已为现有记录设置默认刷新频率：1.0小时")
        else:
            print("refresh_frequency 字段已存在，跳过。")
        
except pymysql.Error as e:
    print(f"更新失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

