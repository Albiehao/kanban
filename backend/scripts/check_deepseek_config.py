#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查 DeepSeek 配置"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, DeepSeekConfig

db = SessionLocal()
try:
    config = db.query(DeepSeekConfig).first()
    if config:
        print("当前配置:")
        print(f"  ID: {config.id}")
        print(f"  API密钥: {config.api_key[:4]}****{config.api_key[-4:]}")
        print(f"  每分钟限制: {config.rate_limit_per_minute}")
        print(f"  每日限制: {config.rate_limit_per_day}")
        print(f"  状态: {'已启用' if config.is_active else '已禁用'}")
        print(f"  模型: {config.model}")
    else:
        print("[INFO] 数据库中没有配置")
finally:
    db.close()

