#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试任务API"""

import requests
import json
from datetime import datetime, timedelta

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


def test_get_tasks():
    """测试获取任务列表"""
    print("\n测试获取任务列表...")
    response = requests.get(
        f"{BASE_URL}/api/tasks",
        params={"page": 1, "limit": 10},
        headers=get_headers()
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 获取成功")
        print(f"  - 总任务数: {data['data']['pagination']['total']}")
        print(f"  - 当前页: {data['data']['pagination']['page']}")
        print(f"  - 每页数量: {data['data']['pagination']['limit']}")
        print(f"  - 返回任务数: {len(data['data']['items'])}")
        return True
    else:
        print(f"✗ 获取失败: {response.text}")
        return False


def test_create_task():
    """测试创建任务"""
    print("\n测试创建任务...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    task_data = {
        "title": "测试任务",
        "description": "这是一个测试任务",
        "priority": "high",
        "date": tomorrow,
        "time": "09:00-11:00",
        "has_reminder": True,
        "reminder_time": f"{tomorrow}T08:00:00"
    }
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data,
        headers=get_headers()
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"✓ 创建成功，任务ID: {data['data']['id']}")
        print(f"  - 标题: {data['data']['title']}")
        print(f"  - 日期: {data['data']['date']}")
        print(f"  - 优先级: {data['data']['priority']}")
        return data['data']['id']
    else:
        print(f"✗ 创建失败: {response.text}")
        return None


def test_update_task(task_id):
    """测试更新任务"""
    print(f"\n测试更新任务 {task_id}...")
    update_data = {
        "completed": True,
        "priority": "medium"
    }
    response = requests.put(
        f"{BASE_URL}/api/tasks/{task_id}",
        json=update_data,
        headers=get_headers()
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 更新成功")
        print(f"  - 完成状态: {data['data']['completed']}")
        print(f"  - 优先级: {data['data']['priority']}")
        return True
    else:
        print(f"✗ 更新失败: {response.text}")
        return False


def test_toggle_task(task_id):
    """测试切换任务完成状态"""
    print(f"\n测试切换任务 {task_id} 完成状态...")
    response = requests.patch(
        f"{BASE_URL}/api/tasks/{task_id}/toggle",
        headers=get_headers()
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 切换成功，新状态: {data['data']['completed']}")
        return True
    else:
        print(f"✗ 切换失败: {response.text}")
        return False


def test_delete_task(task_id):
    """测试删除任务"""
    print(f"\n测试删除任务 {task_id}...")
    response = requests.delete(
        f"{BASE_URL}/api/tasks/{task_id}",
        headers=get_headers()
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ 删除成功: {response.json()['message']}")
        return True
    else:
        print(f"✗ 删除失败: {response.text}")
        return False


def test_filter_tasks():
    """测试过滤任务"""
    print("\n测试按条件过滤任务...")
    tomorrow = datetime.now() + timedelta(days=1)
    
    # 创建几个测试任务
    tasks = []
    for i in range(3):
        task_data = {
            "title": f"过滤测试任务 {i+1}",
            "description": f"测试任务描述 {i+1}",
            "priority": "high" if i % 2 == 0 else "low",
            "date": tomorrow.strftime("%Y-%m-%d"),
            "has_reminder": i % 2 == 0
        }
        response = requests.post(
            f"{BASE_URL}/api/tasks",
            json=task_data,
            headers=get_headers()
        )
        if response.status_code == 201:
            tasks.append(response.json()['data']['id'])
    
    # 测试按优先级过滤
    print("\n按优先级过滤（high）...")
    response = requests.get(
        f"{BASE_URL}/api/tasks",
        params={"page": 1, "limit": 10, "priority": "high"},
        headers=get_headers()
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 高优先级任务数: {data['data']['pagination']['total']}")
    
    # 测试按日期过滤
    print(f"\n按日期过滤（{tomorrow.strftime('%Y-%m-%d')}）...")
    response = requests.get(
        f"{BASE_URL}/api/tasks",
        params={"page": 1, "limit": 10, "date": tomorrow.strftime("%Y-%m-%d")},
        headers=get_headers()
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✓ 该日期任务数: {data['data']['pagination']['total']}")
    
    # 清理测试任务
    for task_id in tasks:
        requests.delete(f"{BASE_URL}/api/tasks/{task_id}", headers=get_headers())


def main():
    """主测试函数"""
    print("=" * 60)
    print("任务API测试")
    print("=" * 60)
    
    # 登录
    if not login():
        print("\n无法登录，测试终止")
        return
    
    # 运行测试
    try:
        # 测试获取任务列表
        test_get_tasks()
        
        # 测试创建任务
        task_id = test_create_task()
        if task_id:
            # 测试更新任务
            test_update_task(task_id)
            
            # 测试切换完成状态
            test_toggle_task(task_id)
            
            # 测试删除任务
            test_delete_task(task_id)
        
        # 测试过滤功能
        test_filter_tasks()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n测试过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

