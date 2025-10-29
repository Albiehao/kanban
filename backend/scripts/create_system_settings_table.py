#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建系统设置表"""

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
        print("正在创建系统设置表...")
        
        # 创建表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(50) UNIQUE NOT NULL,
                setting_value TEXT NOT NULL,
                description VARCHAR(200),
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                updated_by INT,
                INDEX idx_key (setting_key)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) FROM system_settings")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("插入默认系统设置...")
            cursor.execute("""
                INSERT INTO system_settings (setting_key, setting_value, description) VALUES
                ('maintenance_mode', 'false', '维护模式开关'),
                ('auto_backup', 'true', '自动备份开关'),
                ('email_notifications', 'true', '邮件通知开关')
            """)
            print("默认设置已插入")
        else:
            print(f"系统中已有 {count} 条设置")
        
        connection.commit()
        print("系统设置表创建成功！")
        
except pymysql.Error as e:
    print(f"创建表失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

