#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试注册功能"""

import requests
import json
import random

BASE_URL = "http://127.0.0.1:8000"

def test_register():
    """测试用户注册"""
    
    # 生成随机用户名和邮箱避免重复
    random_num = random.randint(1000, 9999)
    username = f"testuser{random_num}"
    email = f"test{random_num}@example.com"
    
    # 测试用例1: 正常注册
    print("=" * 60)
    print("测试用例1: 正常注册")
    print("=" * 60)
    
    data = {
        "username": username,
        "email": email,
        "password": "test123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("[SUCCESS] 注册成功!")
            print(f"Token: {result['token'][:50]}...")
            print(f"用户信息: {json.dumps(result['user'], indent=2, ensure_ascii=False)}")
        else:
            print(f"[FAILED] 注册失败: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] 请求出错: {e}")
    
    # 测试用例2: 重复用户名
    print("\n" + "=" * 60)
    print("测试用例2: 重复用户名")
    print("=" * 60)
    
    data = {
        "username": username,  # 使用刚才注册的用户名
        "email": f"another{random_num}@example.com",
        "password": "test123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] 请求出错: {e}")
    
    # 测试用例3: 无效的邮箱格式
    print("\n" + "=" * 60)
    print("测试用例3: 无效的邮箱格式")
    print("=" * 60)
    
    data = {
        "username": f"testuser{random_num + 1}",
        "email": "invalid-email",
        "password": "test123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] 请求出错: {e}")
    
    # 测试用例4: 密码太短
    print("\n" + "=" * 60)
    print("测试用例4: 密码太短")
    print("=" * 60)
    
    data = {
        "username": f"testuser{random_num + 2}",
        "email": f"test{random_num + 2}@example.com",
        "password": "123",  # 太短
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] 请求出错: {e}")
    
    # 测试用例5: 用户名包含非法字符
    print("\n" + "=" * 60)
    print("测试用例5: 用户名包含非法字符")
    print("=" * 60)
    
    data = {
        "username": "user-name",  # 包含连字符
        "email": f"test{random_num + 3}@example.com",
        "password": "test123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] 请求出错: {e}")
    
    # 测试用例6: 注册teacher角色
    print("\n" + "=" * 60)
    print("测试用例6: 注册teacher角色")
    print("=" * 60)
    
    data = {
        "username": f"teacher{random_num}",
        "email": f"teacher{random_num}@example.com",
        "password": "teacher123456",
        "role": "teacher"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("[SUCCESS] 注册成功!")
            print(f"用户角色: {result['user']['role']}")
            print(f"用户权限: {result['user']['permissions']}")
        else:
            print(f"[FAILED] 注册失败: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] 请求出错: {e}")
    
    # 测试用例7: 尝试注册admin角色（应该被降级为student）
    print("\n" + "=" * 60)
    print("测试用例7: 尝试注册admin角色")
    print("=" * 60)
    
    data = {
        "username": f"testadmin{random_num}",
        "email": f"admin{random_num}@example.com",
        "password": "admin123456",
        "role": "admin"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("[SUCCESS] 注册成功!")
            print(f"用户角色: {result['user']['role']} (admin被降级为student)")
    except Exception as e:
        print(f"[ERROR] 请求出错: {e}")

if __name__ == "__main__":
    test_register()

