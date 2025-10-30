#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更新 DeepSeek 限流配置"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, DeepSeekConfig

db = SessionLocal()
try:
    # 获取当前激活的配置
    config = db.query(DeepSeekConfig).filter(DeepSeekConfig.is_active == True).first()
    
    if not config:
        print("未找到激活的配置")
    else:
        # 更新限流配置
        old_min = config.rate_limit_per_minute
        old_day = config.rate_limit_per_day
        
        config.rate_limit_per_minute = 20  # 提高到20次/分钟
        config.rate_limit_per_day = 500    # 提高到500次/天
        
        db.commit()
        db.refresh(config)
        
        print(f"[OK] 限流配置已更新")
        print(f"  每分钟: {old_min} -> {config.rate_limit_per_minute}")
        print(f"  每天: {old_day} -> {config.rate_limit_per_day}")
        
except Exception as e:
    print(f"[ERROR] 更新失败: {e}")
    db.rollback()
finally:
    db.close()

