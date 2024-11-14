# main.py
from fastapi import FastAPI, HTTPException
from data_cache import data_cache
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_crystal_cache  #스크래퍼 크리스탈 불러오기



app = FastAPI()

@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {"message": "Welcome to the ArkLife API"}


@app.get("/items/{category_code}")
async def get_items_by_category(category_code: int):
    if category_code in data_cache:
        return {"Items": data_cache[category_code]}
    raise HTTPException(status_code=404, detail="Category not found")

@app.get("/api/crystal")
async def get_crystal_price():
    crystal_price = get_crystal_cache()  # 함수로 최신 값 가져오기
    if crystal_price is None:
        raise HTTPException(status_code=503, detail="크리스탈 시세 데이터가 아직 준비되지 않았습니다.")
    return {"crystal_price": crystal_price}

origins = [
    "http://localhost:3000",  # 프론트엔드 주소
    "http://arklife.store"
    "http://43.203.231.113",  # 배포된 백엔드 주소
]

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["*"],  # 필요한 도메인으로 제한하는 것이 더 안전합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)