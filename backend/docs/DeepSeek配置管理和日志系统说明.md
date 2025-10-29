# DeepSeek配置管理和日志系统说明

## 一、DeepSeek配置管理（管理员专用）

### 1. 数据库表

**表名**: `deepseek_configs`

**字段**:
- `id`: 主键，自增
- `api_key`: DeepSeek API密钥（必填）
- `base_url`: API基础URL（默认：https://api.deepseek.com）
- `model`: 模型名称（默认：deepseek-chat）
- `is_active`: 是否启用（默认：true）
- `rate_limit_per_minute`: 每分钟请求限制（默认：10）
- `rate_limit_per_day`: 每日请求限制（默认：500）
- `created_at`: 创建时间
- `updated_at`: 更新时间

### 2. API接口（管理员权限）

**基础路径**: `/api/admin/deepseek`

#### 2.1 获取配置列表
- **路径**: `GET /api/admin/deepseek/configs`
- **权限**: 管理员
- **参数**: 
  - `include_inactive` (可选): 是否包含已禁用的配置，默认false
- **返回**: 配置列表

**示例**:
```bash
GET /api/admin/deepseek/configs?include_inactive=true
Authorization: Bearer <ADMIN_TOKEN>
```

**响应**:
```json
{
  "count": 2,
  "configs": [
    {
      "id": 1,
      "api_key": "sk-9cb****0bb5f",
      "base_url": "https://api.deepseek.com",
      "model": "deepseek-chat",
      "is_active": true,
      "rate_limit_per_minute": 10,
      "rate_limit_per_day": 500,
      ...
    }
  ]
}
```

#### 2.2 获取单个配置
- **路径**: `GET /api/admin/deepseek/config`
- **权限**: 管理员
- **参数**: 
  - `config_id` (可选): 配置ID，不提供则返回当前启用的配置
- **返回**: 配置详情（包含脱敏的API密钥）

#### 2.3 创建配置
- **路径**: `POST /api/admin/deepseek/config`
- **权限**: 管理员
- **请求体**:
```json
{
  "api_key": "sk-xxxxxxxxxxxxx",
  "base_url": "https://api.deepseek.com",
  "model": "deepseek-chat",
  "is_active": true,
  "rate_limit_per_minute": 10,
  "rate_limit_per_day": 500
}
```
- **返回**: 创建的配置详情

**注意**: 
- 如果创建时 `is_active=true`，且已有启用的配置，会返回错误
- 创建配置会自动记录warning级别日志

#### 2.4 更新配置
- **路径**: `PUT /api/admin/deepseek/config/{config_id}`
- **权限**: 管理员
- **请求体**: 同创建，所有字段可选
- **返回**: 更新后的配置详情

**注意**: 
- 如果更新 `is_active=true`，会自动禁用其他启用的配置
- 更新配置会自动记录warning级别日志

#### 2.5 删除配置
- **路径**: `DELETE /api/admin/deepseek/config/{config_id}`
- **权限**: 管理员
- **返回**: 删除成功消息

**注意**: 
- 删除配置会自动记录warning级别日志（包含配置的部分信息）

#### 2.6 切换配置状态
- **路径**: `POST /api/admin/deepseek/config/{config_id}/toggle`
- **权限**: 管理员
- **返回**: 更新后的配置详情

**注意**: 
- 启用配置时会自动禁用其他启用的配置
- 切换状态会自动记录warning级别日志

---

## 二、日志系统优化

### 1. 日志保存策略

**规则**: 只保存 **warning** 和 **error** 级别的日志到数据库，**info** 级别只输出到控制台。

**原因**:
- 减少数据库存储压力
- info级别日志通常量很大，但重要性较低
- warning和error级别的日志更重要，需要持久化

### 2. LogService 更新

**位置**: `app/services/log_service.py`

**修改**:
- `add_log()` 方法：自动过滤info级别
- `get_logs()` 方法：默认只返回warning和error

**使用示例**:
```python
from app.services.log_service import LogService

log_service = LogService(db)

# info级别：只打印到控制台，不保存到数据库
log_service.add_log("用户登录", level="info", module="auth")

# warning级别：保存到数据库 + 控制台
log_service.add_log("API密钥过期", level="warning", module="deepseek_config")

# error级别：保存到数据库 + 控制台
log_service.add_log("数据库连接失败", level="error", module="database")
```

### 3. 查询日志

**接口**: `GET /api/admin/logs`

**参数**:
- `level` (可选): "warning" 或 "error"，不能是 "info"
- `limit` (可选): 返回数量，默认50，最大200

**注意**: 如果查询 `level=info`，会返回错误，因为数据库中不存在info级别日志。

---

## 三、使用流程

### 1. 初始化数据库表

运行初始化脚本：
```bash
python scripts/create_deepseek_config_table.py
```

### 2. 创建第一个配置（通过API）

```bash
POST /api/admin/deepseek/config
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json

{
  "api_key": "sk-9cb005b49aae4cba91a717cf8420bb5f",
  "base_url": "https://api.deepseek.com",
  "model": "deepseek-chat"
}
```

### 3. 管理配置

- **查看所有配置**: `GET /api/admin/deepseek/configs`
- **更新配置**: `PUT /api/admin/deepseek/config/{id}`
- **删除配置**: `DELETE /api/admin/deepseek/config/{id}`
- **切换状态**: `POST /api/admin/deepseek/config/{id}/toggle`

### 4. 查看日志

```bash
GET /api/admin/logs?level=warning&limit=100
Authorization: Bearer <ADMIN_TOKEN>
```

---

## 四、安全说明

### 1. 权限控制
- 所有配置管理接口都需要管理员权限（admin 或 super_admin）
- 普通用户无法访问

### 2. API密钥脱敏
- 查询接口返回的API密钥会自动脱敏（显示为 `sk-9cb****0bb5f`）
- 创建和更新时需要提供完整密钥

### 3. 操作日志
- 所有配置操作都会记录日志（warning级别）
- 日志包含操作者、操作类型、配置ID等信息

---

## 五、向后兼容

### 1. 配置读取
- DeepSeekService 会自动从数据库读取配置
- 如果数据库中没有配置，会使用默认值或环境变量
- 保证系统正常运行

### 2. 默认配置
- 如果数据库未配置，使用：
  - 默认API密钥（硬编码）
  - 环境变量 `DEEPSEEK_API_KEY`（如果设置了）
  - 其他默认值

### 3. 日志兼容
- 旧的日志调用不受影响
- info级别日志仍然会输出到控制台
- 只是不会保存到数据库

---

## 六、注意事项

1. **配置唯一性**: 同一时间只能有一个启用的配置
2. **API密钥安全**: 不要在前端直接显示完整密钥
3. **日志清理**: 建议定期清理过期的warning/error日志
4. **权限验证**: 所有配置管理接口都已添加管理员权限检查

---

**文档版本**: v1.0.0  
**创建日期**: 2025-10-29

