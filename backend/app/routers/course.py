"""课程路由"""

from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import CourseCreate, CourseUpdate
from app.database import get_db
from app.auth import get_current_active_user
from app.services.edu_binding_service import EduBindingService
import requests

router = APIRouter(prefix="/api/courses", tags=["课程表"])

@router.get("")
async def get_courses(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """从第三方API获取当前用户的课程"""
    # 获取用户的API配置（从数据库）
    edu_service = EduBindingService(db)
    binding = edu_service.get_binding_for_crawler(current_user.id)
    
    if not binding:
        print(f"[INFO] 用户 {current_user.id} 未绑定API密钥")
        return {"data": [], "error": "未绑定API密钥，请先配置"}
    
    api_key = binding.get("api_key")
    api_url = binding.get("api_url", "http://160.202.229.142:8000/api/v1/api/courses")
    
    print(f"[INFO] 使用API配置: URL={api_url}, Key={api_key[:4]}***")
    
    # 调用第三方API
    try:
        headers = {"X-API-Key": api_key}
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # 第三方API返回格式: {"header": {...}, "data": [...]}
            # 提取data字段直接返回给前端
            courses = result.get("data", [])
            return {"data": courses}
        else:
            return {"data": [], "error": f"第三方API错误: {response.status_code}"}
            
    except Exception as e:
        return {"data": [], "error": f"获取课程失败: {str(e)}"}


@router.post("", status_code=201)
async def create_course(
    course: CourseCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建课程（已弃用，使用第三方API）"""
    raise HTTPException(
        status_code=400,
        detail="课程数据由第三方API提供，无法手动创建"
    )


@router.put("/{course_id}")
async def update_course(
    course_id: int,
    course: CourseUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新课程（暂不支持，建议先删除再创建）"""
    raise HTTPException(status_code=501, detail="课程更新功能尚未实现")


@router.delete("/{course_id}", status_code=204)
async def delete_course(
    course_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除指定课程（已弃用，课程由第三方API管理）"""
    raise HTTPException(
        status_code=400,
        detail="课程数据由第三方API提供，无法删除"
    )


@router.post("/crawl")
async def crawl_courses(crawl_data: Dict):
    """从第三方API爬取课程（已弃用）"""
    raise HTTPException(
        status_code=400,
        detail="请使用 /api/courses/fetch-from-edu 接口"
    )


@router.post("/batch")
async def batch_import_courses(
    courses_data: Dict,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """批量导入课程（符合需求文档路径）
    
    注意：由于课程数据主要从第三方API获取，此接口主要用于前端
    批量提交课程数据到后端进行处理或验证，实际保存由第三方API管理
    """
    courses = courses_data.get("courses", [])
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供courses数组"
        )
    
    # 验证课程数据格式
    validated_courses = []
    errors = []
    
    for idx, course_data in enumerate(courses):
        try:
            # 验证必要字段
            if not course_data.get("course_name"):
                errors.append({"index": idx, "error": "课程名称不能为空", "course": course_data})
                continue
            
            validated_courses.append({
                "course_name": course_data.get("course_name"),
                "classroom": course_data.get("classroom"),
                "teacher": course_data.get("teacher"),
                "date": course_data.get("date"),
                "periods": course_data.get("periods")
            })
        except Exception as e:
            errors.append({"index": idx, "error": str(e), "course": course_data})
    
    # 由于课程由第三方API管理，这里只返回验证结果
    # 实际保存需要调用第三方API
    return {
        "success": True,
        "message": f"验证完成，有效课程: {len(validated_courses)} 条",
        "validated": len(validated_courses),
        "errors": len(errors),
        "data": {
            "valid": validated_courses,
            "invalid": errors
        }
    }


@router.post("/import")
async def import_courses(
    courses_data: Dict,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """导入课程数据（已弃用，使用第三方API）"""
    raise HTTPException(
        status_code=400,
        detail="课程数据由第三方API自动提供"
    )


@router.post("/fetch-from-edu")
async def fetch_courses_from_edu(
    crawl_config: Dict,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """从第三方API获取课程数据
    
    请求体示例:
    {
        "start_date": "2024-09-01",  // 可选
        "end_date": "2024-12-31",     // 可选
        "week": 1                     // 可选
    }
    """
    edu_service = EduBindingService(db)
    binding = edu_service.get_binding_for_crawler(current_user.id)
    
    if not binding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未绑定API密钥"
        )
    
    api_key = binding.get("api_key")
    api_url = binding.get("api_url", "http://160.202.229.142:8000/api/v1/api/courses")
    
    # 查询参数
    params = {}
    if crawl_config.get("start_date"):
        params["start_date"] = crawl_config["start_date"]
    if crawl_config.get("end_date"):
        params["end_date"] = crawl_config["end_date"]
    if crawl_config.get("week"):
        params["week"] = crawl_config["week"]
    
    # 调用第三方API
    try:
        headers = {"X-API-Key": api_key}
        response = requests.get(
            api_url,
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            # 第三方API返回格式: {"header": {...}, "data": [...]}
            # 提取data字段返回给前端
            courses = result.get("data", [])
            return {
                "success": True,
                "message": "课程获取成功",
                "courses": courses
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"第三方API错误: {response.text}"
            )
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取课程失败: {str(e)}"
        )


@router.get("/my-courses")
async def get_my_courses(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的课程（从第三方API）"""
    return await get_courses(current_user, db)


@router.delete("/my-courses")
async def delete_my_courses(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除当前用户的所有课程（已弃用）"""
    raise HTTPException(
        status_code=400,
        detail="课程数据由第三方API管理，无法删除"
    )

