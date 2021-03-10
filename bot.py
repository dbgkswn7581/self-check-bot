import discord
from discord.ext import commands
import os
import time
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

#한국 표준 시간으로 변경하기 (호스팅 시에만 필요함)
def get_time():
    global now, timon, tiday, tihour
    
    now = time.localtime() 
    timon = now.tm_mon
    tiday = now.tm_mday
    tihour = now.tm_hour
    tihour = tihour + 9

    if tihour >= 24:
        tihour = tihour - 24
        tiday += 1
        if timon == 3:
            if tiday >= 32:
                tiday = 1
                timon += 1
        elif timon ==  4 :
            if tiday >=  31 :
                tiday = 1
                timon += 1
        elif timon ==  5 :
            if tiday >=  32 :
                tiday = 1
                timon += 1
        elif timon ==  6 :
            if tiday >=  31 :
                tiday = 1
                timon += 1
        elif timon ==  7 :
            if tiday >=  32 :
                tiday = 1
                timon += 1
        elif timon ==  8 :
            if tiday >=  32 :
                tiday = 1
                timon += 1
        elif timon ==  9 :
            if tiday >=  31 :
                tiday = 1
                timon += 1
        elif timon ==  10 :
            if tiday >=  32 :
                tiday = 1
                timon += 1
        elif timon ==  11 :
            if tiday >=  31 :
                tiday = 1
                timon += 1
        elif timon ==  12 :
            if tiday >=  32 :
                tiday = 1
                timon += 1
        elif timon ==  1 :
            if tiday >=  32 :
                tiday = 1
                timon += 1
        elif timon ==  2 :
            if tiday >=  29 :
                tiday = 1
                timon += 1

#오늘 날짜 
def set_today():
    global today
    get_time()

    today_year = str(int(now.tm_year))
    today_month = timon
    today_day = tiday


    if len(str(today_month)) == 1:
        today_month = '0' + str(today_month)
    else:
        today_month = str(today_month)

    if len(str(today_day)) == 1:
        today_day = '0' + str(today_day)
    else:
        today_day = str(today_day)

    today = today_year+today_month+today_day

    print("today is ", end='')
    print(today)

#자가진단 사이트 접속
# 변수 : province, sch_level, sch_name, name, yymmdd, psd
def self_check():
    url = "https://hcs.eduro.go.kr/#/loginHome"

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="btnConfirm2"]').click() #시작화면에서 시작 버튼 클릭

    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr[1]/td/button').click() # 학교 검색 버튼 
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
      

    return meals




#================================================================================================================================================
client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():

    print("==============READY===================")
    game = discord.Game("자가진단 매크로 테스트")
    await client.change_presence(status = discord.Status.online, activity = game)

@client.event
async def on_message(ctx):
    if ctx.content == "#내정보":
        user = ctx.author
        await ctx.channel.send(f"{user.name} / {user.id}")
    
    if ctx.content == "#진단":
        a = self_check()
        if a[:2] == "1.":
            embed = discord.Embed(title = "Success",
            description = "자가진단 예/아니요 페이지 진입 성공", color = discord.Color.blue()
            )
            await ctx.send(embed=embed)

        else:
            print(a[:2])
            print(a)
            await ctx.channel.send(a)


client.run(os.environ['token'])