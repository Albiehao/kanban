# 用户列表和服务器信息API说明

## ✅ 功能概述

后端已完全支持：
1. **获取用户列表** - 管理员可查看所有用户
2. **获取服务器信息** - 跨平台支持（Linux/Windows），包括CPU、内存、磁盘、网络等信息

## 📋 API 接口

### 1. 获取用户列表

**请求:**
```http
GET /api/admin/users
Authorization: Bearer {token}
```

**权限要求:**
- 管理员（admin）或超级管理员（super_admin）

**响应:**
```json
{
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "is_active": true,
      "bio": null,
      "avatar_url": null,
      "created_at": "2025-10-28T10:00:00",
      "updated_at": "2025-10-28T10:00:00"
    },
    {
      "id": 2,
      "username": "user1",
      "email": "user1@example.com",
      "role": "user",
      "is_active": true,
      "bio": null,
      "avatar_url": null,
      "created_at": "2025-10-28T11:00:00",
      "updated_at": "2025-10-28T11:00:00"
    }
  ]
}
```

**错误响应:**
```json
{
  "detail": "需要管理员权限"
}
```
状态码: 403

### 2. 获取服务器信息

**请求:**
```http
GET /api/admin/server/info
Authorization: Bearer {token}
```

**权限要求:**
- 管理员（admin）或超级管理员（super_admin）

**响应:**
```json
{
  "data": {
    "platform": {
      "system": "Windows",  // 或 "Linux", "Darwin" 等
      "platform": "Windows-10-10.0.26100-SP0",
      "machine": "AMD64",
      "processor": "Intel64 Family 6 Model 158 Stepping 10, GenuineIntel",
      "python_version": "3.11.0"
    },
    "resources": {
      "cpu": {
        "count": 8,
        "usage_percent": 25.5,
        "frequency_mhz": 2800.0,
        "max_frequency_mhz": 4500.0
      },
      "memory": {
        "total_gb": 16.0,
        "used_gb": 8.5,
        "available_gb": 7.5,
        "usage_percent": 53.1
      },
      "disk": {
        "total_gb": 500.0,
        "used_gb": 250.0,
        "free_gb": 250.0,
        "usage_percent": 50.0
      },
      "uptime": {
        "days": 5,
        "hours": 12,
        "minutes": 30,
        "formatted": "5天 12小时 30分钟"
      },
      "boot_time": "2025-10-23 10:00:00"
    },
    "network": {
      "bytes_sent_gb": 125.5,
      "bytes_recv_gb": 234.8,
      "packets_sent": 12345678,
      "packets_recv": 23456789
    },
    "application": {
      "python_version": "3.11.0 (tags/v3.11.0:deaf509, Oct  3 2023, 00:00:00) [MSC v.1934 64 bit (AMD64)]",
      "working_directory": "G:\\play\\todo\\backend",
      "server_time": "2025-10-28 15:30:00"
    }
  }
}
```

**跨平台支持:**
- ✅ **Windows**: 自动检测当前驱动器（如 C: 盘）
- ✅ **Linux**: 使用根目录 `/`
- ✅ **macOS**: 使用根目录 `/`

**错误响应:**
```json
{
  "detail": "需要管理员权限"
}
```
状态码: 403

## 🔧 技术实现

### 跨平台磁盘检测

```python
import platform
import os

if platform.system() == 'Windows':
    # Windows: 获取当前驱动器
    current_drive = os.path.splitdrive(os.getcwd())[0]
    disk = psutil.disk_usage(current_drive)
else:
    # Linux/Mac: 使用根目录
    disk = psutil.disk_usage('/')
```

### 依赖库

- **psutil**: 跨平台系统资源监控库（已在 requirements.txt 中）
  - CPU使用率、核心数、频率
  - 内存使用情况
  - 磁盘使用情况
  - 网络IO统计
  - 系统启动时间

### 错误处理

如果 `psutil` 未安装或获取失败：
- 返回占位数据或错误信息
- 不会导致API崩溃
- 提供友好的错误提示

## 📊 使用示例

### Python 示例

```python
import requests

# 登录获取token
response = requests.post("http://localhost:8000/api/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
token = response.json()["token"]

headers = {"Authorization": f"Bearer {token}"}

# 获取用户列表
response = requests.get(
    "http://localhost:8000/api/admin/users",
    headers=headers
)
users = response.json()["data"]
print(f"用户总数: {len(users)}")

# 获取服务器信息
response = requests.get(
    "http://localhost:8000/api/admin/server/info",
    headers=headers
)
server_info = response.json()["data"]
print(f"操作系统: {server_info['platform']['system']}")
print(f"CPU使用率: {server_info['resources']['cpu']['usage_percent']}%")
print(f"内存使用率: {server_info['resources']['memory']['usage_percent']}%")
print(f"磁盘使用率: {server_info['resources']['disk']['usage_percent']}%")
print(f"系统运行时间: {server_info['resources']['uptime']['formatted']}")
```

### cURL 示例

```bash
# 登录获取token
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.token')

# 获取用户列表
curl -X GET "http://localhost:8000/api/admin/users" \
  -H "Authorization: Bearer $TOKEN"

# 获取服务器信息
curl -X GET "http://localhost:8000/api/admin/server/info" \
  -H "Authorization: Bearer $TOKEN"
```

### JavaScript/TypeScript 示例

```typescript
// 获取用户列表
async function getUsers() {
  const response = await fetch('http://localhost:8000/api/admin/users', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const result = await response.json();
  return result.data;
}

// 获取服务器信息
async function getServerInfo() {
  const response = await fetch('http://localhost:8000/api/admin/server/info', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  const result = await response.json();
  return result.data;
}

// 使用示例
const users = await getUsers();
console.log(`用户总数: ${users.length}`);

const serverInfo = await getServerInfo();
console.log(`操作系统: ${serverInfo.platform.system}`);
console.log(`CPU使用率: ${serverInfo.resources.cpu.usage_percent}%`);
console.log(`内存使用率: ${serverInfo.resources.memory.usage_percent}%`);
console.log(`磁盘使用率: ${serverInfo.resources.disk.usage_percent}%`);
console.log(`系统运行时间: ${serverInfo.resources.uptime.formatted}`);
```

## 🛡️ 安全特性

1. **权限验证**: 只有管理员和超级管理员可以访问
2. **用户隔离**: 用户列表只返回基本信息，不包含敏感数据
3. **错误处理**: 完善的异常处理，不会泄露系统敏感信息

## 📝 注意事项

1. **psutil 依赖**: 
   - 已在 `requirements.txt` 中包含 `psutil==5.9.6`
   - 如果未安装，API仍可工作但返回占位数据

2. **跨平台兼容性**:
   - Windows: 自动检测当前工作驱动器
   - Linux/Mac: 使用根目录
   - 其他平台: 会尝试使用根目录

3. **性能考虑**:
   - CPU使用率获取需要0.5秒间隔，确保准确性
   - 其他信息实时获取

## ✅ 总结

- ✅ **用户列表**: `/api/admin/users` - 获取所有用户
- ✅ **服务器信息**: `/api/admin/server/info` - 跨平台系统信息
- ✅ **跨平台支持**: Windows 和 Linux 均已测试
- ✅ **权限控制**: 仅管理员可访问
- ✅ **错误处理**: 完善的异常处理机制

后端已完全支持用户列表和服务器信息功能！🎉

