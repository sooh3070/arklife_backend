import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 캐싱할 데이터 변수
crystal_cache = None

# 크리스탈 시세를 가져오는 함수
def fetch_crystal_data():
    global crystal_cache
    driver = None  # 초기화
    try:
        # Selenium WebDriver 설정
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Headless 모드 실행
        chrome_options.add_argument("--no-sandbox")  # 권한 문제 방지
        chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 공간 부족 방지
        chrome_options.add_argument("--disable-gpu")  # GPU 비활성화 (헤드리스 환경에서 필요)
        chrome_options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트 설정

        # ChromeDriver 경로
        driver_path = "./bin/chromedriver"

        # Service 객체를 통해 ChromeDriver 경로 전달
        service = Service(executable_path=driver_path)

        # WebDriver 초기화
        driver = webdriver.Chrome(service=service, options=chrome_options)

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
