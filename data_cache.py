# data_cache.py
import requests
import time
from threading import Thread

API_BASE_URL = 'https://developer-lostark.game.onstove.com'
JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDA1NjY1NTIifQ.JdyWXbgAOQZMnIWXSXrB-ZEmqgHILQVzpr_VblnPA-aS7ORwd_UJMJ6v-9CXDKeQ14DtUC864OZ9IXL3jYJz0W8exzxwkKj747A704ce-3CvHWTnueWgn8lBfoV49EDYLTT-D6Ud5JXiPIL0iqx-hh4bn_TImqHaLDs4ZD3aFGu5vEcQoVk4RrevkhB8mbLPjjPQDc0tAXchcBLkBfxT3fjyhzYWCUPvZ6jsgplin_3H-hcdc2JKmjqP_JsTRU050PlS4jbQwC5Xq7Wz3zYKzPtHjJtYNM91eApE21-spsQGRD8pILoFKA9h3vjbb9bo83mSjrwnNPEImccGMYVFHg'
 # 실제 JWT 토큰을 입력하세요

# 캐싱할 데이터 딕셔너리
data_cache = {}

# Lost Ark API로부터 데이터 가져오기
def fetch_items_by_category(category_code):
    try:
        headers = {
            'Authorization': f'bearer {JWT_TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "Sort": "GRADE",
            "CategoryCode": category_code,
            "PageNo": 1,
            "SortCondition": "ASC"
        }
        response = requests.post(f"{API_BASE_URL}/markets/items", json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("Items", [])  # Items 배열 반환
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data for category {category_code}: {e}")
        return []

# 주기적으로 Lost Ark API 데이터를 업데이트
def update_data_cache():
    while True:
        # 업데이트할 카테고리 코드 리스트
        category_codes = [90200, 90300, 90400, 90500, 90700]
        for code in category_codes:
            data_cache[code] = fetch_items_by_category(code)
        print("Data cache updated.")
        time.sleep(60)  # 1분 대기

# 데이터 캐시를 백그라운드에서 지속적으로 업데이트
cache_thread = Thread(target=update_data_cache)
cache_thread.daemon = True
cache_thread.start()
