#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建交易记录表"""

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
        print("正在创建交易记录表...")
        
        # 检查表是否已存在
        cursor.execute("SHOW TABLES LIKE 'transactions'")
        if cursor.fetchone():
            print("交易记录表已存在，将检查索引...")
            
            # 检查索引是否存在
            cursor.execute("SHOW INDEX FROM transactions WHERE Key_name = 'idx_user_date'")
            if not cursor.fetchone():
                cursor.execute("CREATE INDEX idx_user_date ON transactions(user_id, date)")
                print("已创建索引 idx_user_date")
            
            # MySQL函数索引可能需要特定版本，跳过检查
            # 月份查询会使用 idx_user_date 索引
            
            connection.commit()
            print("交易记录表索引检查完成")
        else:
            # 创建表
            cursor.execute("""
                CREATE TABLE transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type ENUM('income', 'expense') NOT NULL COMMENT '类型：收入或支出',
                    amount DECIMAL(10, 2) NOT NULL COMMENT '金额',
                    category VARCHAR(50) NOT NULL COMMENT '类别',
                    description VARCHAR(255) NOT NULL COMMENT '描述',
                    date DATE NOT NULL COMMENT '交易日期',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                    INDEX idx_user_date (user_id, date),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='交易记录表'
            """)
            
            connection.commit()
            print("交易记录表创建成功！")
        
except pymysql.Error as e:
    print(f"创建表失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

