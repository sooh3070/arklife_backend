from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scraper import get_crystal_cache  #스크래퍼 크리스탈 불러오기


if __name__ == "__main__":
    ab = get_crystal_cache()
    print(ab)