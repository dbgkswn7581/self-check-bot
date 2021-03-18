import discord
from discord.ext import commands
import os
import time
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


def copy_input(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)




client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():

    print("==============READY===================")
    game = discord.Game("자가진단 매크로 테스트")
    await client.change_presence(status = discord.Status.online, activity = game)

@client.command(name="경로")
async def account(ctx):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com') 


    usr = "yhj7581"
    pwd = "gkswn758123"

    copy_input('//*[@id="id"]',usr)
    time.sleep(0.5)
    copy_input('//*[@id="pw"]',pwd)
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



client.run("ODE0MzExODc5MzA3NTU4OTQy.YDcBCQ.K3UqVc_KCj0orIPL_rfEeSdgkBA")
