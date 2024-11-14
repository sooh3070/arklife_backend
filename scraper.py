# crystal_data_cache.py
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


from webdriver_manager.chrome import ChromeDriverManager
import os

# 캐싱할 데이터 변수
crystal_cache = None

# 크리스탈 시세를 가져오는 함수
def fetch_crystal_data():
    global crystal_cache
    driver = None  # 초기화
    try:
        # Selenium WebDriver 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        os.environ['WD_MANAGER_PATH'] = '/app/.wdm'
        os.environ['WDM_LOCAL'] = '1'  # 로컬 경로 사용
        os.environ['WDM_LOG_LEVEL'] = '0'  # 로그를 최소화
        os.environ['WDM_CACHE_DIR'] = '/app/.wdm'  # 캐시 디렉토리 변경
        os.environ['WDM_LOCAL'] = "/app/.wdm"
        
        driver_path = "/app/.wdm"  # 애플리케이션 디렉토리로 변경
        print(f"Creating directory at {driver_path}")
        os.makedirs(driver_path, exist_ok=True)
        print(f"Directory {driver_path} created successfully")

        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(driver_version="130.0.6723.117").install()),
            options=chrome_options
        )
        
        # 목표 URL에 접속
        url = 'https://loatool.taeu.kr/lospi/'
        driver.get(url)
        
        # 페이지 로드 대기
        time.sleep(3)
        
        # 첫 번째 값 추출
        elements = driver.find_elements(By.CLASS_NAME, "text-h6")
        strings = [element.text for element in elements]
        crystal_cache = int(strings[0].replace(",", ""))
        print(f"Data updated: {crystal_cache}")  # 디버그용 출력

    except Exception as e:
        print(f"Failed to fetch crystal data: {e}")
        
    finally:
        if driver:  # 드라이버가 초기화된 경우에만 종료
            driver.quit()

# 주기적으로 크리스탈 데이터를 업데이트하는 함수
def update_crystal_cache():
    while True:
        fetch_crystal_data()
        print(f"data update: {crystal_cache}")
        time.sleep(120)

# 최신 crystal_cache 값을 반환하는 함수
def get_crystal_cache():
    return crystal_cache

# 데이터 캐시를 백그라운드에서 지속적으로 업데이트
cache_thread = Thread(target=update_crystal_cache)
cache_thread.daemon = True
cache_thread.start()
