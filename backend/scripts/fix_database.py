#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复数据库角色枚举"""

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
        print("正在更新数据库角色枚举...")
        
        # 先清理现有数据
        cursor.execute("DELETE FROM users")
        print("已清理旧数据")
        
        # 删除旧表
        cursor.execute("DROP TABLE IF EXISTS users")
        print("已删除旧表")
        
        connection.commit()
        
        # 重新创建表（将在应用程序启动时自动创建）
        print("将在应用启动时自动创建新表")
        print("数据库准备完成！")
        
except pymysql.Error as e:
    print(f"更新失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

