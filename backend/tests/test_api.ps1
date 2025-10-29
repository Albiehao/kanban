# PowerShell 测试登录脚本

# 方法1: 使用 Invoke-RestMethod（推荐）
$body = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

Write-Host "Login Response:" -ForegroundColor Green
$response | ConvertTo-Json -Depth 5

# 保存token用于后续请求
$global:token = $response.token
Write-Host "`nToken saved to `$global:token" -ForegroundColor Yellow

# 方法2: 使用 Invoke-WebRequest
Write-Host "`n--- Testing other endpoints ---" -ForegroundColor Cyan

# 测试健康检查
$health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
Write-Host "Health Check: $($health.status)" -ForegroundColor Green

# 测试获取任务
$tasks = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/tasks"
Write-Host "Found $($tasks.Count) tasks" -ForegroundColor Green

# 测试获取课程
$courses = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/courses"
Write-Host "Found $($courses.total) courses" -ForegroundColor Green

