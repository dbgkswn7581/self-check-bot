import os
import time
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

url = "https://hcs.eduro.go.kr/#/loginHome"

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    
driver = webdriver.Chrome("D:/selfcheck_bot/chromedriver.exe")

driver.get(url)

driver.find_element_by_xpath('//*[@id="btnConfirm2"]').click() #시작화면에서 시작 버튼 클릭

time.sleep(1)

driver.find_element_by_xpath('//*[@id="schul_name_input"]').click() # 학교 검색 버튼 
driver.find_element_by_xpath('//*[@id="sidolabel"]').click() # 시/도 선택 버튼
driver.find_element_by_xpath('//*[@id="sidolabel"]/option[14]').click() # 전라북도 버튼
driver.find_element_by_xpath('//*[@id="crseScCode"]').click() #학교급 선택 버튼
driver.find_element_by_xpath('//*[@id="crseScCode"]/option[5]').click() #고등학교 버튼
schname = driver.find_element_by_xpath('//*[@id="orgname"]') # 학교 이름 선택 버튼
schname.click()
schname.send_keys("전라고등학교")
schname.send_keys(Keys.RETURN)
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a/span').click() #학교 선택
driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[2]/input').click() #학교선택 버튼 클릭

inputname = driver.find_element_by_xpath('//*[@id="user_name_input"]') #이름 입력 칸 클릭
inputname.click()
inputname.send_keys("유한주")

inputdate = driver.find_element_by_xpath('//*[@id="birthday_input"]') #생년월일 입력 칸 클릭
inputdate.click()
inputdate.send_keys("031210")

driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()

time.sleep(1)

inputpsd = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr/td/input')
inputpsd.click()
inputpsd.send_keys('6213')

driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()

time.sleep(2)

driver.find_element_by_xpath('//*[@id="container"]/div/section[2]/div[2]/ul/li/a/em').click()

time.sleep(2)


# ===================================BeautifulSoup==========================================

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')

meals = soup.select_one('#survey_q1').get_text()

print(meals)
