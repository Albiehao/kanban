"""爬虫工具基类"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests


class Crawler(ABC):
    """爬虫工具基类
    
    所有爬虫工具都应该继承这个基类，实现统一的接口
    """
    
    def __init__(self, timeout: int = 30):
        """初始化爬虫
        
        Args:
            timeout: 请求超时时间（秒）
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @abstractmethod
    def parse_data(self, content: str) -> List[Dict]:
        """解析数据（子类必须实现）
        
        Args:
            content: 原始内容
            
        Returns:
            解析后的数据列表
        """
        pass
    
    def fetch(self, url: str, headers: Dict[str, str] = None) -> str:
        """获取网页内容
        
        Args:
            url: 目标URL
            headers: 自定义请求头
            
        Returns:
            HTML内容
            
        Raises:
            requests.RequestException: 请求失败
        """
        combined_headers = {**self.default_headers, **(headers or {})}
        
        response = self.session.get(url, headers=combined_headers, timeout=self.timeout)
        response.raise_for_status()
        
        return response.text
    
    def fetch_json(self, url: str, headers: Dict[str, str] = None) -> Dict:
        """获取JSON数据
        
        Args:
            url: 目标URL
            headers: 自定义请求头
            
        Returns:
            JSON数据
            
        Raises:
            requests.RequestException: 请求失败
        """
        combined_headers = {**self.default_headers, **(headers or {})}
        
        response = self.session.get(url, headers=combined_headers, timeout=self.timeout)
        response.raise_for_status()
        
        return response.json()
    
    def crawl(self, source: str, source_type: str = "url") -> List[Dict]:
        """爬取数据
        
        Args:
            source: 数据源（URL、JSON字符串或文本）
            source_type: 源类型 (url, json, text, html)
            
        Returns:
            解析后的数据列表
        """
        try:
            if source_type == "url":
                content = self.fetch(source)
                return self.parse_data(content)
            elif source_type == "json":
                return self.parse_data(source)
            elif source_type == "text":
                return self.parse_data(source)
            else:
                print(f"不支持的源类型: {source_type}")
                return []
        except Exception as e:
            print(f"爬取数据失败: {e}")
            return []
    
    def close(self):
        """关闭会话"""
        self.session.close()

