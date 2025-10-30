#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建低频率 DeepSeek 配置"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, DeepSeekConfig
from datetime import datetime

API_KEY = "sk-4d6437333a7549eeab648a367817d4a2"

db = SessionLocal()
try:
    # 检查是否已有配置
    existing = db.query(DeepSeekConfig).first()
    if existing:
        print("[INFO] 配置已存在")
        print(f"  ID: {existing.id}")
        print(f"  API密钥: {existing.api_key[:4]}****{existing.api_key[-4:]}")
        print(f"  每分钟限制: {existing.rate_limit_per_minute}")
    else:
        # 创建新配置，使用低频率避免 governor 错误
        config = DeepSeekConfig(
            api_key=API_KEY,
            base_url="https://api.deepseek.com",
            model="deepseek-chat",
            is_active=True,
            rate_limit_per_minute=2,  # 降低到2次/分钟
            rate_limit_per_day=100,   # 降低到100次/天
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(config)
        db.commit()
        db.refresh(config)
        
        print("[OK] 配置创建成功")
        print(f"  ID: {config.id}")
        print(f"  API密钥: {config.api_key[:4]}****{config.api_key[-4:]}")
        print(f"  每分钟限制: {config.rate_limit_per_minute}")
        print(f"  每日限制: {config.rate_limit_per_day}")
        print(f"  状态: 已启用")
        print()
        print("提示: 使用低频率配置以避免 governor 错误")
        
except Exception as e:
    print(f"[ERROR] 操作失败: {e}")
    db.rollback()
finally:
    db.close()

