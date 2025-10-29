#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""初始化课程数据到数据库"""

import pymysql
import json
from datetime import datetime

# 数据库配置
DB_USER = "root"
DB_PASSWORD = "12345678"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "todo_db"

# 获取第一个用户ID
try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    with connection.cursor() as cursor:
        # 获取第一个用户
        cursor.execute("SELECT id FROM users ORDER BY id LIMIT 1")
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            print(f"使用用户ID: {user_id} 导入课程数据...")
            
            # 示例课程数据
            courses = [
                {"course_name": "软件工程", "classroom": "好学楼B209", "date": "2025-10-28", "teacher": "孙锦程", "periods": "1-2节"},
                {"course_name": "操作系统", "classroom": "好学楼B210", "date": "2025-10-28", "teacher": "刘丹", "periods": "8-10节"},
                {"course_name": "移动应用开发技术", "classroom": "力行楼B409", "date": "2025-10-29", "teacher": "聂小燕", "periods": "3-5节"},
                {"course_name": "马克思主义基本原理", "classroom": "德润讲堂", "date": "2025-10-29", "teacher": "陈惠珍", "periods": "3-4节"},
                {"course_name": "JavaEE基础", "classroom": "力行楼A400", "date": "2025-10-29", "teacher": "孙宁", "periods": "6-7节"},
            ]
            
            # 批量插入课程
            insert_count = 0
            for course in courses:
                cursor.execute("""
                    INSERT INTO courses (user_id, course_name, classroom, date, teacher, periods, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                """, (
                    user_id,
                    course["course_name"],
                    course["classroom"],
                    course["date"],
                    course["teacher"],
                    course["periods"]
                ))
                insert_count += 1
            
            connection.commit()
            print(f"成功导入 {insert_count} 门课程到数据库！")
        else:
            print("未找到用户，请先创建用户")
        
except pymysql.Error as e:
    print(f"导入失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

