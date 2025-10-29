"""
Todo Backend API - 主入口文件
"""
from fastapi import FastAPI
import uvicorn

from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
