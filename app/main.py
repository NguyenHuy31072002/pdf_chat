from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI()

# Đăng ký router cho các endpoint
app.include_router(router)



# Lệnh chạy :   uvicorn app.main:app --reload