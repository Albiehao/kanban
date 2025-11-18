#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
登录功能完整示例
演示如何使用登录API以及访问受保护的接口
"""

import requests
import json
from typing import Optional, Dict, Any

BASE_URL = "http://127.0.0.1:8000"


class TodoClient:
    """Todo API客户端"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.headers: Dict[str, str] = {}
    
    def login(self, username: str, password: str) -> bool:
        """用户登录"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data["token"]
                self.headers = {"Authorization": f"Bearer {self.token}"}
                print(f"[SUCCESS] 登录成功!")
                print(f"用户: {data['user'].get('username')}")
                print(f"角色: {data['user'].get('role')}")
                return True
            else:
                print(f"[FAILED] 登录失败: {response.json()}")
                return False
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return False
    
    def verify(self) -> Optional[Dict]:
        """验证Token"""
        try:
            response = requests.get(
                f"{self.base_url}/api/auth/verify",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                print("[SUCCESS] Token验证成功")
                print(f"用户信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return data
            else:
                print(f"[FAILED] Token验证失败: {response.json()}")
                return None
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None
    
    def get_tasks(self) -> Optional[list]:
        """获取任务列表"""
        try:
            response = requests.get(
                f"{self.base_url}/api/tasks",
                headers=self.headers
            )
            if response.status_code == 200:
                result = response.json()
                items = result.get('data', {}).get('items', [])
                print(f"[SUCCESS] 获取到 {len(items)} 个任务")
                return items
            else:
                print(f"[FAILED] 获取任务失败: {response.json()}")
                return None
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None
    
    def get_courses(self) -> Optional[dict]:
        """获取课程列表"""
        try:
            response = requests.get(
                f"{self.base_url}/api/courses",
                headers=self.headers
            )
            if response.status_code == 200:
                result = response.json()
                courses = result.get('data', [])
                print(f"[SUCCESS] 获取到 {len(courses)} 个课程")
                return courses
            else:
                print(f"[FAILED] 获取课程失败: {response.json()}")
                return None
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None
    
    def get_transactions(self) -> Optional[list]:
        """获取交易记录"""
        try:
            response = requests.get(
                f"{self.base_url}/api/transactions",
                headers=self.headers
            )
            if response.status_code == 200:
                result = response.json()
                transactions = result.get('data', [])
                print(f"[SUCCESS] 获取到 {len(transactions)} 条交易记录")
                return transactions
            else:
                print(f"[FAILED] 获取交易记录失败: {response.json()}")
                return None
        except Exception as e:
            print(f"[ERROR] 请求失败: {e}")
            return None
    
    # 注：当前后端未实现登出和刷新Token接口，示例中不包含这些步骤


def main():
    """主函数 - 演示完整的使用流程"""
    print("=" * 60)
    print("Todo API 登录示例")
    print("=" * 60)
    
    # 创建客户端
    client = TodoClient()
    
    # 测试默认账户登录
    print("\n1. 使用super_admin账户登录")
    print("-" * 60)
    if not client.login("super_admin", "super_admin"):
        print("登录失败，无法继续")
        return
    
    # 验证token
    print("\n2. 验证Token")
    print("-" * 60)
    client.verify()
    
    # 获取任务列表
    print("\n3. 获取任务列表")
    print("-" * 60)
    tasks = client.get_tasks()
    if tasks:
        print(f"示例任务: {tasks[0].get('title', 'N/A') if tasks else 'N/A'}")
    
    # 获取课程列表
    print("\n4. 获取课程列表")
    print("-" * 60)
    courses = client.get_courses()
    
    # 获取交易记录
    print("\n5. 获取交易记录")
    print("-" * 60)
    transactions = client.get_transactions()
    
    # 注：演示结束，不包含刷新Token和登出步骤
    
    print("\n" + "=" * 60)
    print("演示完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()

