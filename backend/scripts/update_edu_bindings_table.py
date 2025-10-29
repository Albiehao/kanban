#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更新教务系统绑定表结构 - 改为存储API Key"""

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
        # 检查是否存在 edu_username 和 edu_password 列
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'edu_account_bindings'
        """, (DB_NAME,))
        columns = [row[0] for row in cursor.fetchall()]
        
        # 如果存在旧字段，删除它们
        if 'edu_username' in columns or 'edu_password' in columns:
            print("删除旧字段: edu_username, edu_password...")
            if 'edu_username' in columns:
                cursor.execute("ALTER TABLE edu_account_bindings DROP COLUMN edu_username")
            if 'edu_password' in columns:
                cursor.execute("ALTER TABLE edu_account_bindings DROP COLUMN edu_password")
        
        # 检查是否存在 api_key 列
        if 'api_key' not in columns:
            print("添加新字段: api_key...")
            cursor.execute("ALTER TABLE edu_account_bindings ADD COLUMN api_key VARCHAR(255) NOT NULL AFTER user_id")
        
        connection.commit()
        print("[成功] 表结构更新完成！")
        
except pymysql.Error as e:
    print(f"[失败] 更新表结构失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

