#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""禁用 DeepSeek 配置（当 API 密钥无效时）"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, DeepSeekConfig

db = SessionLocal()
try:
    config = db.query(DeepSeekConfig).first()
    if config:
        if config.is_active:
            config.is_active = False
            db.commit()
            print("[OK] DeepSeek 配置已禁用")
            print(f"配置 ID: {config.id}")
            print(f"API 密钥: {config.api_key[:4]}****{config.api_key[-4:]}")
        else:
            print("[INFO] DeepSeek 配置已经是禁用状态")
    else:
        print("[ERROR] 未找到 DeepSeek 配置")
except Exception as e:
    print(f"[ERROR] 操作失败: {e}")
    db.rollback()
finally:
    db.close()

