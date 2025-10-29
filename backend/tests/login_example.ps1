# Todo API 登录示例 - PowerShell版本

# 测试登录功能

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Todo API 登录示例" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$baseUrl = "http://127.0.0.1:8000"

# 1. 登录
Write-Host "`n1. 使用admin账户登录" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Gray

$loginData = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod `
        -Uri "$baseUrl/api/auth/login" `
        -Method Post `
        -ContentType "application/json" `
        -Body $loginData
    
    $token = $loginResponse.token
    $headers = @{
        Authorization = "Bearer $token"
    }
    
    Write-Host "[SUCCESS] 登录成功!" -ForegroundColor Green
    Write-Host "用户: $($loginResponse.user.username)" -ForegroundColor White
    Write-Host "角色: $($loginResponse.user.role)" -ForegroundColor White
    Write-Host "权限: $($loginResponse.user.permissions -join ', ')" -ForegroundColor White
}
catch {
    Write-Host "[ERROR] 登录失败: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. 验证Token
Write-Host "`n2. 验证Token" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Gray

try {
    $verifyResponse = Invoke-RestMethod `
        -Uri "$baseUrl/api/auth/verify" `
        -Method Get `
        -Headers $headers
    
    Write-Host "[SUCCESS] Token验证成功" -ForegroundColor Green
    Write-Host "用户信息:" -ForegroundColor White
    $verifyResponse | ConvertTo-Json -Depth 5
}
catch {
    Write-Host "[ERROR] Token验证失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 3. 获取任务列表
Write-Host "`n3. 获取任务列表" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Gray

try {
    $tasks = Invoke-RestMethod `
        -Uri "$baseUrl/api/tasks" `
        -Method Get `
        -Headers $headers
    
    Write-Host "[SUCCESS] 获取到 $($tasks.Count) 个任务" -ForegroundColor Green
    if ($tasks.Count -gt 0) {
        Write-Host "示例任务: $($tasks[0].title)" -ForegroundColor White
    }
}
catch {
    Write-Host "[ERROR] 获取任务失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 4. 获取课程列表
Write-Host "`n4. 获取课程列表" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Gray

try {
    $courses = Invoke-RestMethod `
        -Uri "$baseUrl/api/courses" `
        -Method Get `
        -Headers $headers
    
    Write-Host "[SUCCESS] 获取到 $($courses.total) 个课程" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] 获取课程失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 5. 获取交易记录
Write-Host "`n5. 获取交易记录" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Gray

try {
    $transactions = Invoke-RestMethod `
        -Uri "$baseUrl/api/transactions" `
        -Method Get `
        -Headers $headers
    
    Write-Host "[SUCCESS] 获取到 $($transactions.Count) 条交易记录" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] 获取交易记录失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 6. 刷新Token
Write-Host "`n6. 刷新Token" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Gray

try {
    $refreshResponse = Invoke-RestMethod `
        -Uri "$baseUrl/api/auth/refresh" `
        -Method Post `
        -Headers $headers
    
    $newToken = $refreshResponse.token
    Write-Host "[SUCCESS] Token刷新成功" -ForegroundColor Green
    Write-Host "新Token: $($newToken.Substring(0, 50))..." -ForegroundColor White
}
catch {
    Write-Host "[ERROR] Token刷新失败: $($_.Exception.Message)" -ForegroundColor Red
}

# 7. 登出
Write-Host "`n7. 用户登出" -ForegroundColor Yellow
Write-Host "--------------------------------" -ForegroundColor Gray

try {
    $logoutResponse = Invoke-RestMethod `
        -Uri "$baseUrl/api/auth/logout" `
        -Method Post `
        -Headers $headers
    
    Write-Host "[SUCCESS] 登出成功" -ForegroundColor Green
    Write-Host "响应: $($logoutResponse.message)" -ForegroundColor White
}
catch {
    Write-Host "[ERROR] 登出失败: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "演示完成!" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

