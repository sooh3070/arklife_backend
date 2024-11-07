# main.py
from fastapi import FastAPI, HTTPException
from data_cache import data_cache
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/items/{category_code}")
async def get_items_by_category(category_code: int):
    if category_code in data_cache:
        return {"Items": data_cache[category_code]}
    raise HTTPException(status_code=404, detail="Category not found")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 도메인으로 제한하는 것이 더 안전합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)