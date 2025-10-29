#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""初始化数据库"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from sqlalchemy import create_engine

# 数据库配置
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "todo_db"

def create_database():
    """创建数据库"""
    try:
        # 连接MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"数据库 {DB_NAME} 创建成功或已存在")
        
        connection.close()
        
        # 创建表
        from app.database import create_tables
        create_tables()
        print("数据表创建成功")
        
    except pymysql.Error as e:
        print(f"数据库创建失败: {e}")
        print("\n请确保:")
        print("1. MySQL服务正在运行")
        print("2. MySQL用户名和密码正确")
        print("3. 已安装pymysql: pip install pymysql")
        return False
    
    return True

if __name__ == "__main__":
    create_database()

