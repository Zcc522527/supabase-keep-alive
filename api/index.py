from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum
from supabase import create_client, Client
import os

app = FastAPI()

@app.get("/api")
async def keepalive(key: str = Query(..., description="Access key")):
    """Keepalive endpoint"""
    # 验证访问密钥
    access_key = os.getenv("ACCESS_KEY")
    if not access_key or key != access_key:
        return JSONResponse(
            status_code=403,
            content={"status": "error", "message": "Unauthorized"}
        )
    
    try:
        # 获取环境变量
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        table_name = os.getenv("TABLE_NAME")
        
        if not all([supabase_url, supabase_key, table_name]):
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Missing env variables"}
            )
        
        # 连接 Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # 执行查询
        response = supabase.table(table_name).select("*").limit(1).execute()
        
        return {
            "status": "success",
            "message": "Keepalive ping successful",
            "table": table_name
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "message": "Service is running"}

# 🔥 关键：Vercel 需要这个 handler
handler = Mangum(app)
