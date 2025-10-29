#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试管理员API"""

import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = None


def login():
    """登录获取token"""
    global TOKEN
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": "super_admin", "password": "super_admin"}
    )
    if response.status_code == 200:
        TOKEN = response.json()["token"]
        print(f"✓ 登录成功，token: {TOKEN[:50]}...")
        return True
    else:
        print(f"✗ 登录失败: {response.text}")
        return False


def get_headers():
    """获取请求头"""
    return {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def test_get_users():
    """测试获取用户列表"""
    print("\n测试获取用户列表...")
    response = requests.get(
        f"{BASE_URL}/api/admin/users",
        headers=get_headers()
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 获取成功")
        print(f"  - 用户数量: {len(data.get('data', []))}")
        if data.get('data'):
            print(f"  - 第一个用户: {data['data'][0].get('username')}")
        return True
    else:
        print(f"✗ 获取失败: {response.text}")
        return False


def test_get_server_info():
    """测试获取服务器信息"""
    print("\n测试获取服务器信息...")
    response = requests.get(
        f"{BASE_URL}/api/admin/server/info",
        headers=get_headers()
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 获取成功")
        server_info = data.get('data', {})
        platform = server_info.get('platform', {})
        resources = server_info.get('resources', {})
        
        print(f"  - 操作系统: {platform.get('system')}")
        print(f"  - Python版本: {platform.get('python_version')}")
        
        if 'cpu' in resources:
            print(f"  - CPU使用率: {resources['cpu'].get('usage_percent')}%")
        if 'memory' in resources:
            print(f"  - 内存使用率: {resources['memory'].get('usage_percent')}%")
        if 'disk' in resources:
            print(f"  - 磁盘使用率: {resources['disk'].get('usage_percent')}%")
        if 'uptime' in resources:
            print(f"  - 运行时间: {resources['uptime'].get('formatted')}")
        
        return True
    else:
        print(f"✗ 获取失败: {response.text}")
        return False


def test_cors():
    """测试CORS配置"""
    print("\n测试CORS配置...")
    # 测试 OPTIONS 预检请求
    response = requests.options(
        f"{BASE_URL}/api/admin/users",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization"
        }
    )
    print(f"OPTIONS请求状态码: {response.status_code}")
    print(f"CORS响应头:")
    cors_headers = {
        'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
        'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
        'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
    }
    for key, value in cors_headers.items():
        print(f"  {key}: {value}")
    
    if cors_headers.get('Access-Control-Allow-Origin') == '*' or 'localhost:3000' in str(cors_headers.get('Access-Control-Allow-Origin', '')):
        print("✓ CORS配置正确")
        return True
    else:
        print("✗ CORS配置可能有问题")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("管理员API测试")
    print("=" * 60)
    
    # 登录
    if not login():
        print("\n无法登录，测试终止")
        return
    
    # 运行测试
    try:
        # 测试CORS
        test_cors()
        
        # 测试获取用户列表
        test_get_users()
        
        # 测试获取服务器信息
        test_get_server_info()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n测试过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

