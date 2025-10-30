#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更新DeepSeek API密钥"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, DeepSeekConfig

def update_api_key(new_api_key: str):
    """更新DeepSeek API密钥
    
    Args:
        new_api_key: 新的API密钥
    """
    if not new_api_key or not new_api_key.startswith('sk-'):
        print("错误: API密钥格式不正确，应以 'sk-' 开头")
        return False
    
    db = SessionLocal()
    try:
        config = db.query(DeepSeekConfig).first()
        if config:
            old_key = config.api_key
            print(f"当前密钥: {old_key[:4]}****{old_key[-4:]}")
            print(f"更新为:    {new_api_key[:4]}****{new_api_key[-4:]}")
            
            config.api_key = new_api_key
            db.commit()
            
            print(f"\n[OK] 更新成功！")
            print(f"新密钥: {new_api_key[:4]}****{new_api_key[-4:]}")
            
            # 刷新配置
            db.refresh(config)
            print(f"配置状态: {'已启用' if config.is_active else '已禁用'}")
            return True
        else:
            print("[ERROR] 未找到配置文件")
            print("请先通过管理后台创建DeepSeek配置")
            return False
    except Exception as e:
        print(f"[ERROR] 更新失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("DeepSeek API密钥更新工具")
    print("=" * 60)
    print()
    
    # 从命令行参数获取密钥
    if len(sys.argv) > 1:
        new_key = sys.argv[1]
    else:
        # 交互式输入
        print("请输入新的DeepSeek API密钥:")
        print("(可以从 https://platform.deepseek.com/api_keys 获取)")
        print()
        new_key = input("API Key: ").strip()
    
    if new_key:
        update_api_key(new_key)
    else:
        print("[ERROR] 未提供API密钥")
    
    print()
    print("=" * 60)
    print("提示: 更新后需要重启服务器才能生效")
    print("=" * 60)

