#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建通知表"""

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
        print("正在创建通知表...")
        
        # 检查表是否已存在
        cursor.execute("SHOW TABLES LIKE 'notifications'")
        if cursor.fetchone():
            print("通知表已存在，跳过创建")
        else:
            cursor.execute("""
                CREATE TABLE notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type VARCHAR(50) NOT NULL COMMENT '通知类型：task_reminder, system等',
                    title VARCHAR(255) NOT NULL COMMENT '通知标题',
                    message TEXT COMMENT '通知内容',
                    read BOOLEAN DEFAULT FALSE NOT NULL COMMENT '是否已读',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    INDEX idx_user_id (user_id),
                    INDEX idx_read (read),
                    INDEX idx_user_read (user_id, read),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='通知表';
            """)
            connection.commit()
            print("通知表创建成功！")
        
except pymysql.Error as e:
    print(f"创建表失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

