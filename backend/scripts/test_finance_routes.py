#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试财务路由是否正常注册"""

from app.main import app

print("=" * 50)
print("财务路由检查")
print("=" * 50)

# 获取所有路由
finance_routes = []
other_routes = []

for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        path = route.path
        methods = ', '.join(sorted(route.methods))
        
        if 'transaction' in path.lower() or 'finance' in path.lower():
            finance_routes.append((path, methods))
        else:
            other_routes.append((path, methods))

print("\n✅ 财务相关路由:")
for path, methods in finance_routes:
    print(f"  {methods:10} {path}")

if not finance_routes:
    print("  ❌ 没有找到财务相关路由！")
    print("\n⚠️  请检查:")
    print("  1. app/routers/finance.py 是否存在")
    print("  2. app/routers/finance_stats.py 是否存在")
    print("  3. app/main.py 中是否正确注册了路由")
    print("  4. 服务器是否已重启")
else:
    print(f"\n✅ 找到 {len(finance_routes)} 个财务路由")

print("\n" + "=" * 50)
print("其他路由（前10个）:")
print("=" * 50)
for path, methods in other_routes[:10]:
    print(f"  {methods:10} {path}")


