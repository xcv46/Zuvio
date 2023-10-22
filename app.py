from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time
from bs4 import BeautifulSoup
import random

# 'https://irs.zuvio.com.tw/student5/irs/rollcall/XXXXXX'
URL = 'ENTER_YOUR_COURSE_URL'
EMAIL = 'ENTER_YOUR_EMAIL'
PASSWORD = 'ENTER_YOUR_PASSWORD'
CHROME_DRIVER_PATH = 'ENTER_YOUR_CHROME_DRIVER_PATH'    # 輸入你的chromedriver路徑
HEADLESS = False     #TRUE:不開啟瀏覽器 FALSE:開啟瀏覽器

def login(driver):
    logging.info("進入登入頁")
    driver.get("https://irs.zuvio.com.tw/") #取得登入頁面
    driver.find_element(By.ID, "email").send_keys(EMAIL)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-btn").submit()

def run():
    options = Options()
    options.headless = HEADLESS
    options.binary_location = CHROME_DRIVER_PATH
    LOGGER.setLevel(logging.WARNING)
    driver = webdriver.Chrome(options=options)

    login(driver)
    driver.get(URL)

    logging.info("STARTING LOOP")
    while True:
        PageSource = driver.page_source
        soup = BeautifulSoup(PageSource, 'html.parser') #beautifulsoup 取得網頁原始碼
        result = soup.find("div", class_="irs-rollcall")    #soup.find 找到class為irs-rollcall的div
        logging.debug(result)
        if "準時" in str(result):
            return True
        if "簽到開放中" in str(result):
            logging.info("點名中")
            driver.find_element(By.ID, "submit-make-rollcall").click()  #找到id為submit-make-rollcall的按鈕並點擊
        else:
            logging.info("無點名資訊")
            driver.refresh()
        time.sleep(random.randint(3, 7))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
    run()
    logging.info("選課循環階段結束")
