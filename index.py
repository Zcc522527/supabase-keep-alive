Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:37:50) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from supabase import create_client, Client
import os

app = FastAPI()

@app.get("/api")
async def keepalive(key: str = Query(..., description="Access key for authentication")):
    """
    Keepalive endpoint to prevent Supabase database from going idle.
    """
    # 验证访问密钥
    access_key = os.getenv("ACCESS_KEY")
    if not access_key or key != access_key:
        raise HTTPException(
            status_code=403,
            detail={"status": "error", "message": "Unauthorized: Invalid access key"}
        )
    
    try:
        # 获取环境变量
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        table_name = os.getenv("TABLE_NAME")
        
        # 验证环境变量
        if not all([supabase_url, supabase_key, table_name]):
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "message": "Missing required environment variables"
                }
            )
        
        # 连接 Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # 执行简单查询（只取一条记录）
        response = supabase.table(table_name).select("*").limit(1).execute()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Keepalive ping successful",
                "table": table_name,
                "records_checked": len(response.data) if response.data else 0
            }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Database query failed: {str(e)}"
            }
        )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Supabase Keep-Alive Service is running",
        "endpoint": "/api?key=YOUR_ACCESS_KEY"
    }
