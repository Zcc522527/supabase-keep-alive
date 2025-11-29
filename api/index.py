from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from mangum import Mangum
import os

# 初始化 FastAPI
app = FastAPI()

@app.get("/api")
async def keepalive(key: str = Query(...)):
    """Keepalive endpoint to prevent Supabase database from going idle"""
    
    # 验证访问密钥
    access_key = os.environ.get("ACCESS_KEY")
    if not access_key or key != access_key:
        return JSONResponse(
            status_code=403,
            content={"status": "error", "message": "Unauthorized"}
        )
    
    try:
        # 延迟导入 supabase(避免初始化时出错)
        from supabase import create_client, Client
        
        # 获取环境变量
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        table_name = os.environ.get("TABLE_NAME")
        
        # 验证环境变量
        if not all([supabase_url, supabase_key, table_name]):
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "message": "Missing required environment variables"
                }
            )
        
        # 连接 Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # 执行查询
        response = supabase.table(table_name).select("*").limit(1).execute()
        
        return {
            "status": "success",
            "message": "Keepalive ping successful",
            "table": table_name,
            "records_checked": len(response.data) if response.data else 0
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Supabase Keep-Alive Service",
        "endpoint": "/api?key=YOUR_ACCESS_KEY"
    }

# 🔥 关键:Vercel Lambda handler
handler = Mangum(app, lifespan="off")
