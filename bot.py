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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pyperclip
import smtplib


def copy_input(driver, xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)

def send_email(driver):
    driver.save_screenshot("Screenshot.png")

    # txt = driver.page_source
    # f = open('source.txt', 'w', encoding="UTF-8")
    # f.write(txt)
    # f.close()             

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('dbgkswn7581@gmail.com', 'szxrergdlwfbifbg')

    msg = MIMEBase('multipart', 'mixed')
    cont = MIMEText("내용 : 본문내용")
    cont['Subject'] = '제목 : 메일 보내기 테스트'
    msg.attach(cont)

    path = r'Screenshot.png'
    part = MIMEBase("application", "octet-stream")
    part.set_payload(open(path, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
            'attachment; filename="%s"' % os.path.basename(path))
    msg.attach(part)


    s.sendmail("dbgkswn7581@gmail.com", 'dbgkswn7581@gmail.com', msg.as_string())
    s.quit()
    # ===================================BeautifulSoup==========================================

    req = driver.page_source

    soup = BeautifulSoup(urllib.request.urlopen(req).read(), 'html.parser')

    meals = soup.select_one('#survey_q1').get_text()
      

    return meals


client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():

    print("==============READY===================")
    game = discord.Game("자가진단 매크로 테스트")
    await client.change_presence(status = discord.Status.online, activity = game)

@client.command(name="경로")
async def account(ctx):
    embed = discord.Embed(title = "실행 중...",
    color = discord.Color.green()
    )
    await ctx.channel.send(embed=embed)
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com') 


        usr = "yhj7581"
        pwd = "gkswn758123"

        copy_input(driver, '//*[@id="id"]',usr)
        time.sleep(0.5)
        copy_input(driver, '//*[@id="pw"]',pwd)
        time.sleep(0.5)

        final_btn = driver.find_element_by_xpath('//*[@id="log.login"]')
        final_btn.click()
        time.sleep(2)

        driver.get('https://mybox.naver.com/')
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="list_area"]/div/div[2]/div/ul/li[8]/label/a/div/div[1]/div').click()
        # driver.find_element_by_xpath('//*[@id="content_wrap"]/div[2]/input').send_keys(r"D:/selfcheck_bot/테스트용.txt")

        embed = discord.Embed(title = "가입",
        description = os.path.abspath('.'), color = discord.Color.gold()
        )

        await ctx.send(embed=embed)

        embed = discord.Embed(title = "가입",
        description = os.getcwd(), color = discord.Color.gold()
        )

        await ctx.send(embed=embed)

    except Exception as ex:
            
            embed = discord.Embed(title = "Failed",
            description = "#BeatifulSoup", color = discord.Color.red()
            )
            await ctx.channel.send(embed=embed)
            await ctx.channel.send(ex)
            send_email(driver)


client.run(os.environ['token'])
