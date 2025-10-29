# Agent工具格式修复说明

## 问题

错误信息：
```
Error code: 400 - {'error': {'message': 'Failed to deserialize the JSON body into the target type: tools[0]: missing field type at line 1 column 2308', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_request_error'}}
```

## 原因

在 `app/services/agent/agent.py` 中，构建工具列表时只提取了 `function` 部分：

```python
tools_list = [f["function"] for f in functions]  # ❌ 错误：只提取了function部分
```

这导致传递给DeepSeek API的工具定义缺少 `type: "function"` 字段。

## 修复

改为传递完整的工具定义：

```python
tools_list = functions  # ✅ 正确：传递完整工具定义，包含type和function字段
```

## 工具定义格式

正确的格式应该是：

```json
{
  "type": "function",
  "function": {
    "name": "get_tasks",
    "description": "获取用户的任务列表",
    "parameters": {
      "type": "object",
      "properties": {...},
      "required": []
    }
  }
}
```

## 验证

修复后，工具定义已经包含：
- ✅ `type: "function"` 字段
- ✅ `function` 对象，包含 `name`, `description`, `parameters`

现在应该可以正常工作了。

