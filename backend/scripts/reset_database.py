#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""重置数据库 - 删除所有表和数据"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        print("=" * 60)
        print("数据库重置工具")
        print("=" * 60)
        print()
        
        # 获取所有表
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        if not tables:
            print("[INFO] 数据库中没有表")
            print("[INFO] 数据库已经是干净状态")
        else:
            print(f"[INFO] 发现 {len(tables)} 个表")
            print()
            
            # 删除所有表
            print("正在删除所有表...")
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                print(f"  - 已删除表: {table}")
            
            connection.commit()
            print()
            print("[OK] 所有表已删除")
        
        print()
        print("=" * 60)
        print("数据库重置完成！")
        print("=" * 60)
        print()
        print("下一步：")
        print("1. 重新运行 init_database.py 初始化数据库")
        print("2. 或者直接启动服务器，表会自动创建")
        print()
        
except pymysql.Error as e:
    print(f"[ERROR] 操作失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

