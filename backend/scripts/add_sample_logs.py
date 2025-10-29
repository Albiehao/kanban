#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""添加示例系统日志"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, SystemLog
from datetime import datetime

db = SessionLocal()

try:
    logs = [
        SystemLog(
            level="info",
            message="系统启动成功",
            module="system",
            timestamp=datetime.now()
        ),
        SystemLog(
            level="info",
            message="超级管理员登录系统",
            module="auth",
            user_id=1,
            timestamp=datetime.now()
        ),
        SystemLog(
            level="warning",
            message="磁盘使用率达到70%",
            module="monitor",
            timestamp=datetime.now()
        ),
        SystemLog(
            level="info",
            message="备份任务已完成",
            module="backup",
            timestamp=datetime.now()
        ),
        SystemLog(
            level="error",
            message="数据库连接失败",
            module="database",
            timestamp=datetime.now()
        )
    ]
    
    for log in logs:
        db.add(log)
    
    db.commit()
    print(f"已添加 {len(logs)} 条示例日志")
    
except Exception as e:
    print(f"添加日志失败: {e}")
    db.rollback()
finally:
    db.close()

