# CORS配置和API更新说明

## ✅ 后端CORS配置

后端已正确配置CORS，允许所有来源的请求：

```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ 允许所有来源，包括 http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # ✅ 允许所有HTTP方法
    allow_headers=["*"],  # ✅ 允许所有请求头
)
```

**说明：**
- `allow_origins=["*"]` 已经允许包括 `http://localhost:3000` 在内的所有前端域名
- CORS配置位于路由注册之前，确保所有接口都生效

## 📋 API接口更新

### 旧接口（已废弃）

**`GET /api/admin/data`** - 不再推荐使用

这个接口仍存在但返回所有数据（用户列表、服务器信息、系统设置、日志等），建议分别调用新接口。

### 新接口（推荐使用）

#### 1. 获取用户列表

**`GET /api/admin/users`**

**请求:**
```http
GET /api/admin/users
Authorization: Bearer {token}
```

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
    }
  ]
}
```

#### 2. 获取服务器信息

**`GET /api/admin/server/info`**

**请求:**
```http
GET /api/admin/server/info
Authorization: Bearer {token}
```

**响应:**
```json
{
  "data": {
    "platform": {
      "system": "Windows",
      "platform": "Windows-10-10.0.26100-SP0",
      "machine": "AMD64",
      "processor": "...",
      "python_version": "3.11.0"
    },
    "resources": {
      "cpu": {
        "count": 8,
        "usage_percent": 25.5,
        "frequency_mhz": 2800.0
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
      "python_version": "3.11.0 ...",
      "working_directory": "G:\\play\\todo\\backend",
      "server_time": "2025-10-28 15:30:00"
    }
  }
}
```

## 🔍 验证CORS配置

### 测试方法

1. **直接测试CORS预检请求：**

```bash
# 测试 OPTIONS 请求（CORS预检）
curl -X OPTIONS "http://localhost:8000/api/admin/users" \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: authorization" \
  -v
```

应该看到响应头包含：
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

2. **测试实际请求：**

```bash
# 测试 GET 请求
curl -X GET "http://localhost:8000/api/admin/users" \
  -H "Origin: http://localhost:3000" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -v
```

### 如果仍有CORS问题

#### 可能原因1：浏览器缓存

**解决：**
- 清除浏览器缓存
- 使用无痕模式测试
- 按 `Ctrl+Shift+R` 强制刷新

#### 可能原因2：服务器未重启

**解决：**
```bash
# 停止服务器
# 重新启动
python -m uvicorn app.main:app --reload
```

#### 可能原因3：端口不一致

**检查：**
- 前端请求的端口是否正确（通常是8000）
- 后端是否在正确的端口运行

## 🔧 优化CORS配置（可选）

如果需要更严格的CORS配置（生产环境推荐），可以修改为：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 前端开发环境
        "http://localhost:5173",  # Vite默认端口
        "https://yourdomain.com",  # 生产环境域名
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
```

**注意：** 当前配置 `allow_origins=["*"]` 已经足够，如果仍有CORS问题，可能是其他原因。

## 📝 前端调用示例

### Vue.js / TypeScript

```typescript
// adminApi.ts
export const adminApi = {
  // 获取用户列表
  async getUsers(): Promise<User[]> {
    const response = await fetch('http://localhost:8000/api/admin/users', {
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data; // 提取 data 字段
  },

  // 获取服务器信息
  async getServerInfo(): Promise<ServerInfo> {
    const response = await fetch('http://localhost:8000/api/admin/server/info', {
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.data; // 提取 data 字段
  }
};

// 在组件中使用
async function loadAdminData() {
  try {
    // 分别调用两个接口
    const [users, serverInfo] = await Promise.all([
      adminApi.getUsers(),
      adminApi.getServerInfo()
    ]);
    
    console.log('用户列表:', users);
    console.log('服务器信息:', serverInfo);
  } catch (error) {
    console.error('加载管理员数据失败:', error);
    // 处理错误，单个接口失败不影响其他
  }
}
```

### 使用 axios

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器添加token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const adminApi = {
  async getUsers() {
    const response = await api.get('/api/admin/users');
    return response.data.data; // 提取 data 字段
  },

  async getServerInfo() {
    const response = await api.get('/api/admin/server/info');
    return response.data.data; // 提取 data 字段
  }
};
```

## ✅ 验证清单

- [x] CORS已配置，允许所有来源（`allow_origins=["*"]`）
- [x] `/api/admin/users` 接口已实现
- [x] `/api/admin/server/info` 接口已实现
- [x] 接口返回格式统一：`{data: {...}}`
- [x] 权限验证：仅管理员可访问
- [x] 跨平台支持：服务器信息在Windows和Linux上正常工作

## 🚀 测试步骤

1. **启动后端服务器：**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. **测试用户列表接口：**
   ```bash
   curl -X GET "http://localhost:8000/api/admin/users" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **测试服务器信息接口：**
   ```bash
   curl -X GET "http://localhost:8000/api/admin/server/info" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

4. **从浏览器测试（应无CORS错误）：**
   - 打开开发者工具（F12）
   - 查看 Network 标签
   - 前端应能正常调用这两个接口

## 📋 总结

- ✅ **CORS配置正确**：已允许所有来源，包括 `http://localhost:3000`
- ✅ **新接口已实现**：`/api/admin/users` 和 `/api/admin/server/info`
- ✅ **接口格式统一**：都返回 `{data: {...}}` 格式
- ✅ **权限验证完善**：仅管理员可访问
- ✅ **跨平台支持**：服务器信息在Windows和Linux上正常工作

如果仍有CORS错误，请检查：
1. 服务器是否已重启
2. 浏览器缓存是否已清除
3. 前端请求URL是否正确
4. Token是否有效

后端已准备就绪！🎉

