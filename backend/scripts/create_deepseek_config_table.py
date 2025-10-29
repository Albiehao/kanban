"""创建DeepSeek配置表的脚本"""

import pymysql

DB_USER = "root"
DB_PASSWORD = "12345678"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "todo_db"

try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    with connection.cursor() as cursor:
        print("正在创建DeepSeek配置表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deepseek_configs (
                id INT PRIMARY KEY AUTO_INCREMENT,
                api_key VARCHAR(255) NOT NULL COMMENT 'DeepSeek API密钥',
                base_url VARCHAR(255) NOT NULL DEFAULT 'https://api.deepseek.com' COMMENT 'DeepSeek API基础URL',
                model VARCHAR(50) NOT NULL DEFAULT 'deepseek-chat' COMMENT '使用的模型名称',
                is_active BOOLEAN DEFAULT TRUE NOT NULL COMMENT '是否启用',
                rate_limit_per_minute INT DEFAULT 10 NOT NULL COMMENT '每分钟请求限制',
                rate_limit_per_day INT DEFAULT 500 NOT NULL COMMENT '每日请求限制',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                INDEX idx_active (is_active)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='DeepSeek API配置表';
        """)
        connection.commit()
        print("DeepSeek配置表创建成功！")
        
        # 检查是否已有配置，如果没有则插入默认配置
        cursor.execute("SELECT COUNT(*) FROM deepseek_configs WHERE is_active = TRUE")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("插入默认DeepSeek配置...")
            cursor.execute("""
                INSERT INTO deepseek_configs 
                (api_key, base_url, model, is_active, rate_limit_per_minute, rate_limit_per_day)
                VALUES 
                (%s, %s, %s, %s, %s, %s)
            """, (
                "sk-9cb005b49aae4cba91a717cf8420bb5f",
                "https://api.deepseek.com",
                "deepseek-chat",
                True,
                10,
                500
            ))
            connection.commit()
            print("默认配置插入成功！")
        else:
            print(f"已有 {count} 个活跃配置，跳过插入默认配置")
        
except pymysql.Error as e:
    print(f"创建表失败: {e}")
finally:
    if 'connection' in locals():
        connection.close()

