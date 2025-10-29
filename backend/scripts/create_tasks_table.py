#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建任务表"""

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
        print("正在创建任务表...")
        
        # 检查表是否已存在
        cursor.execute("SHOW TABLES LIKE 'tasks'")
        if cursor.fetchone():
            print("任务表已存在，将检查索引...")
            
            # 检查索引是否存在
            cursor.execute("SHOW INDEX FROM tasks WHERE Key_name = 'idx_user_date'")
            if not cursor.fetchone():
                cursor.execute("CREATE INDEX idx_user_date ON tasks(user_id, date)")
                print("已创建索引 idx_user_date")
            
            cursor.execute("SHOW INDEX FROM tasks WHERE Key_name = 'idx_user_completed'")
            if not cursor.fetchone():
                cursor.execute("CREATE INDEX idx_user_completed ON tasks(user_id, completed)")
                print("已创建索引 idx_user_completed")
            
            connection.commit()
            print("任务表索引检查完成")
        else:
            # 创建表
            cursor.execute("""
                CREATE TABLE tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    priority ENUM('high', 'medium', 'low') DEFAULT 'medium',
                    date DATE NOT NULL,
                    time VARCHAR(50),
                    has_reminder BOOLEAN DEFAULT FALSE,
                    reminder_time DATETIME,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_user_date (user_id, date),
                    INDEX idx_user_completed (user_id, completed)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            connection.commit()
            print("任务表创建成功！")
        
except pymysql.Error as e:
    print(f"创建表失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

