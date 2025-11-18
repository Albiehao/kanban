#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试登录功能"""

import requests
import json

# 测试登录
url = "http://127.0.0.1:8000/api/auth/login"
data = {
    "username": "super_admin",
    "password": "super_admin"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("\nResponse:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")

