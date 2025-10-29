#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建系统日志表"""

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
        print("正在创建系统日志表...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                level VARCHAR(20) NOT NULL,
                message VARCHAR(500) NOT NULL,
                module VARCHAR(50),
                user_id INT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_level (level),
                INDEX idx_timestamp (timestamp)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        connection.commit()
        print("系统日志表创建成功！")
        
except pymysql.Error as e:
    print(f"创建表失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

