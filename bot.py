import discord
from discord.ext import commands
import os.path
import os , stat
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
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import psycopg2



#======================================================================================

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

#======================================================================================

#에러 발생
class makeError(Exception):
    def __init__(self):
        super().__init__('Make Error')

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

def send_email(driver):
    driver.save_screenshot("Screenshot.png")

    # txt = driver.page_source
    # f = open('source.txt', 'w', encoding="UTF-8")
    # f.write(txt)
    # f.close()             

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('dbgkswn7581@gmail.com', 'sriojdijqkfgubul')

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

def user_check(id):
    exist = []
    id = str(id)
    con = psycopg2.connect(
        host='ec2-3-222-127-167.compute-1.amazonaws.com', 
        dbname='dc1tl1m2lv0mgi', 
        user='fsnoeuopgcpfpz', 
        password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
        port='5432')

    cur = con.cursor()
    cur.execute("SELECT * FROM user_info;")
    rows = cur.fetchall()

    for i in rows:
        exist.append(i[0])

    if id not in exist:
        con.commit()
        cur.close()
        con.close()
        return 0

    elif id in exist:
        con.commit()
        cur.close()
        con.close()
        return 1
    

     

    


#================================================================================================================================================
client = commands.Bot(command_prefix='#')

@client.event
async def on_ready():

    print("==============READY===================")
    game = discord.Game("'타'가진단")
    await client.change_presence(status = discord.Status.online, activity = game)

@client.command(name="가입")
async def account(ctx, *text):
    try:
        txt = ''
        for tmp in text:
            txt += tmp
            txt += ' '
        info = txt.split()
        
        if len(info) == 0 or len(info) == 1 or len(info) == 2 or len(info) >= 4:
            embed = discord.Embed(title = "잘못 입력하였습니다.",
            description = "다시 입력해주세요.", color = discord.Color.dark_magenta()
            )
            embed.add_field(name="Example", value="#가입 백민혁 030805 1234", inline=False)
            embed.add_field(name="First", value="'백민혁' 부분에는 본인 이름을 입력.", inline=False)
            embed.add_field(name="Second", value="'030805' 부분에는 본인의 생년월일을 YYMMDD 형식으로 입력.", inline=False)
            embed.add_field(name="Third", value="'1234' 부분에는 본인의 자가진단 사이트 비밀번호를 입력.", inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title = "잠시만 기다려주세요...",
            description = " ", color = discord.Color.blue()
            )
            await ctx.send(embed=embed)

            try:
                user_id = ctx.author.id
                check = user_check(str(user_id))
                
                name = str(info[0])
                birth = str(info[1])
                psd = str(info[2])

                print(check, name, birth, psd)

            
            except Exception as ex:
                embed = discord.Embed(title = "Failed",
                description = "#가입 usercheck부분", color = discord.Color.red()
                )
                await ctx.send(embed=embed)
                await ctx.send(ex)

            if len(name) != 3 or len(birth) != 6 or len(psd) != 4:
                embed = discord.Embed(title = "잘못 입력하였습니다.",
                description = "다시 입력해주세요.", color = discord.Color.dark_magenta()
                )
                embed.add_field(name="Example", value="#가입 백민혁 030805 1234", inline=False)
                embed.add_field(name="First", value="'백민혁' 부분에는 본인 이름을 입력.", inline=False)
                embed.add_field(name="Second", value="'030805' 부분에는 본인의 생년월일을 YYMMDD 형식으로 입력.", inline=False)
                embed.add_field(name="Third", value="'1234' 부분에는 본인의 자가진단 사이트 비밀번호를 입력.", inline=False)
                await ctx.send(embed=embed)

            else:
                if check == 0:
                    null = 'NULL'

                    con = psycopg2.connect(
                        host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                        dbname='dc1tl1m2lv0mgi', 
                        user='fsnoeuopgcpfpz', 
                        password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                        port='5432')

                    cur = con.cursor()

                    cur.execute("INSERT INTO user_info (id, name, birth, psd) VALUES (%s, %s, %s, %s);", (user_id, name, birth, psd))

                    con.commit()
                    cur.close()
                    con.close()


                    embed = discord.Embed(title = "가입",
                    description = "개인정보 최초 등록에 성공하였습니다.", color = discord.Color.gold()
                    )

                    embed.add_field(name="이름", value=name, inline=False)
                    embed.add_field(name="생년월일", value=birth, inline=False)
                    embed.add_field(name="비밀번호", value=psd, inline=False)

                    await ctx.send(embed=embed)
                
                elif check == 1:
                    
                    user_id = ctx.author.id

                    con = psycopg2.connect(
                        host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                        dbname='dc1tl1m2lv0mgi', 
                        user='fsnoeuopgcpfpz', 
                        password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                        port='5432')

                    cur = con.cursor()

                    cur.execute("SELECT * FROM user_info WHERE id = '%s'", (user_id,))
                    A_info = cur.fetchall()
                    A_info = str(A_info[0]).replace("'", "").replace(',',"").replace('(',"").replace(')',"").split(" ")

                    con.commit()
                    cur.close()
                    con.close()

                    embed = discord.Embed(title = "가입",
                    description = "이미 개인정보 등록이 되어있습니다.", color = discord.Color.gold()
                    )

                    embed.add_field(name="이름", value=A_info[1], inline=False)
                    embed.add_field(name="생년월일", value=A_info[2], inline=False)
                    embed.add_field(name="비밀번호", value=A_info[3], inline=False)

                    await ctx.send(embed=embed)


    except Exception as ex:
        await ctx.send(ex)

        embed = discord.Embed(title = "Failed",
        description = "#가입 부분", color = discord.Color.red()
        )
        
        await ctx.send(embed=embed)

@client.command(name="ㄱㅇ")
async def account(ctx, *text):
    try:
        txt = ''
        for tmp in text:
            txt += tmp
            txt += ' '
        info = txt.split()
        
        if len(info) == 0 or len(info) == 1 or len(info) == 2 or len(info) >= 4:
            embed = discord.Embed(title = "잘못 입력하였습니다.",
            description = "다시 입력해주세요.", color = discord.Color.dark_magenta()
            )
            embed.add_field(name="Example", value="#가입 백민혁 030805 1234", inline=False)
            embed.add_field(name="First", value="'백민혁' 부분에는 본인 이름을 입력.", inline=False)
            embed.add_field(name="Second", value="'030805' 부분에는 본인의 생년월일을 YYMMDD 형식으로 입력.", inline=False)
            embed.add_field(name="Third", value="'1234' 부분에는 본인의 자가진단 사이트 비밀번호를 입력.", inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title = "잠시만 기다려주세요...",
            description = " ", color = discord.Color.blue()
            )
            await ctx.send(embed=embed)

            try:
                user_id = ctx.author.id
                check = user_check(str(user_id))
                
                name = str(info[0])
                birth = str(info[1])
                psd = str(info[2])

                print(check, name, birth, psd)

            
            except Exception as ex:
                embed = discord.Embed(title = "Failed",
                description = "#가입 usercheck부분", color = discord.Color.red()
                )
                await ctx.send(embed=embed)
                await ctx.send(ex)

            if len(name) != 3 or len(birth) != 6 or len(psd) != 4:
                embed = discord.Embed(title = "잘못 입력하였습니다.",
                description = "다시 입력해주세요.", color = discord.Color.dark_magenta()
                )
                embed.add_field(name="Example", value="#가입 백민혁 030805 1234", inline=False)
                embed.add_field(name="First", value="'백민혁' 부분에는 본인 이름을 입력.", inline=False)
                embed.add_field(name="Second", value="'030805' 부분에는 본인의 생년월일을 YYMMDD 형식으로 입력.", inline=False)
                embed.add_field(name="Third", value="'1234' 부분에는 본인의 자가진단 사이트 비밀번호를 입력.", inline=False)
                await ctx.send(embed=embed)

            else:
                if check == 0:
                    null = 'NULL'

                    con = psycopg2.connect(
                        host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                        dbname='dc1tl1m2lv0mgi', 
                        user='fsnoeuopgcpfpz', 
                        password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                        port='5432')

                    cur = con.cursor()

                    cur.execute("INSERT INTO user_info (id, name, birth, psd) VALUES (%s, %s, %s, %s);", (user_id, name, birth, psd))

                    con.commit()
                    cur.close()
                    con.close()


                    embed = discord.Embed(title = "가입",
                    description = "개인정보 최초 등록에 성공하였습니다.", color = discord.Color.gold()
                    )

                    embed.add_field(name="이름", value=name, inline=False)
                    embed.add_field(name="생년월일", value=birth, inline=False)
                    embed.add_field(name="비밀번호", value=psd, inline=False)

                    await ctx.send(embed=embed)
                
                elif check == 1:
                    
                    user_id = ctx.author.id

                    con = psycopg2.connect(
                        host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                        dbname='dc1tl1m2lv0mgi', 
                        user='fsnoeuopgcpfpz', 
                        password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                        port='5432')

                    cur = con.cursor()

                    cur.execute("SELECT * FROM user_info WHERE id = '%s'", (user_id,))
                    A_info = cur.fetchall()
                    A_info = str(A_info[0]).replace("'", "").replace(',',"").replace('(',"").replace(')',"").split(" ")

                    con.commit()
                    cur.close()
                    con.close()

                    embed = discord.Embed(title = "가입",
                    description = "이미 개인정보 등록이 되어있습니다.", color = discord.Color.gold()
                    )

                    embed.add_field(name="이름", value=A_info[1], inline=False)
                    embed.add_field(name="생년월일", value=A_info[2], inline=False)
                    embed.add_field(name="비밀번호", value=A_info[3], inline=False)

                    await ctx.send(embed=embed)


    except Exception as ex:
        await ctx.send(ex)

        embed = discord.Embed(title = "Failed",
        description = "#가입 부분", color = discord.Color.red()
        )
        
        await ctx.send(embed=embed)
            
@client.command(name="rd")
async def account(ctx, *text):
    try:
        txt = ''
        for tmp in text:
            txt += tmp
            txt += ' '
        info = txt.split()
        
        if len(info) == 0 or len(info) == 1 or len(info) == 2 or len(info) >= 4:
            embed = discord.Embed(title = "잘못 입력하였습니다.",
            description = "다시 입력해주세요.", color = discord.Color.dark_magenta()
            )
            embed.add_field(name="Example", value="#가입 백민혁 030805 1234", inline=False)
            embed.add_field(name="First", value="'백민혁' 부분에는 본인 이름을 입력.", inline=False)
            embed.add_field(name="Second", value="'030805' 부분에는 본인의 생년월일을 YYMMDD 형식으로 입력.", inline=False)
            embed.add_field(name="Third", value="'1234' 부분에는 본인의 자가진단 사이트 비밀번호를 입력.", inline=False)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title = "잠시만 기다려주세요...",
            description = " ", color = discord.Color.blue()
            )
            await ctx.send(embed=embed)

            try:
                user_id = ctx.author.id
                check = user_check(str(user_id))
                
                name = str(info[0])
                birth = str(info[1])
                psd = str(info[2])

                print(check, name, birth, psd)

            
            except Exception as ex:
                embed = discord.Embed(title = "Failed",
                description = "#가입 usercheck부분", color = discord.Color.red()
                )
                await ctx.send(embed=embed)
                await ctx.send(ex)

            if len(name) != 3 or len(birth) != 6 or len(psd) != 4:
                embed = discord.Embed(title = "잘못 입력하였습니다.",
                description = "다시 입력해주세요.", color = discord.Color.dark_magenta()
                )
                embed.add_field(name="Example", value="#가입 백민혁 030805 1234", inline=False)
                embed.add_field(name="First", value="'백민혁' 부분에는 본인 이름을 입력.", inline=False)
                embed.add_field(name="Second", value="'030805' 부분에는 본인의 생년월일을 YYMMDD 형식으로 입력.", inline=False)
                embed.add_field(name="Third", value="'1234' 부분에는 본인의 자가진단 사이트 비밀번호를 입력.", inline=False)
                await ctx.send(embed=embed)

            else:
                if check == 0:
                    null = 'NULL'

                    con = psycopg2.connect(
                        host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                        dbname='dc1tl1m2lv0mgi', 
                        user='fsnoeuopgcpfpz', 
                        password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                        port='5432')

                    cur = con.cursor()

                    cur.execute("INSERT INTO user_info (id, name, birth, psd) VALUES (%s, %s, %s, %s);", (user_id, name, birth, psd))

                    con.commit()
                    cur.close()
                    con.close()


                    embed = discord.Embed(title = "가입",
                    description = "개인정보 최초 등록에 성공하였습니다.", color = discord.Color.gold()
                    )

                    embed.add_field(name="이름", value=name, inline=False)
                    embed.add_field(name="생년월일", value=birth, inline=False)
                    embed.add_field(name="비밀번호", value=psd, inline=False)

                    await ctx.send(embed=embed)
                
                elif check == 1:
                    
                    user_id = ctx.author.id

                    con = psycopg2.connect(
                        host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                        dbname='dc1tl1m2lv0mgi', 
                        user='fsnoeuopgcpfpz', 
                        password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                        port='5432')

                    cur = con.cursor()

                    cur.execute("SELECT * FROM user_info WHERE id = '%s'", (user_id,))
                    A_info = cur.fetchall()
                    A_info = str(A_info[0]).replace("'", "").replace(',',"").replace('(',"").replace(')',"").split(" ")

                    con.commit()
                    cur.close()
                    con.close()

                    embed = discord.Embed(title = "가입",
                    description = "이미 개인정보 등록이 되어있습니다.", color = discord.Color.gold()
                    )

                    embed.add_field(name="이름", value=A_info[1], inline=False)
                    embed.add_field(name="생년월일", value=A_info[2], inline=False)
                    embed.add_field(name="비밀번호", value=A_info[3], inline=False)

                    await ctx.send(embed=embed)


    except Exception as ex:
        await ctx.send(ex)

        embed = discord.Embed(title = "Failed",
        description = "#가입 부분", color = discord.Color.red()
        )
        
        await ctx.send(embed=embed)

# @account.error
# async def account_error(ctx, error):
#     print(error)
#     embed = discord.Embed(title = "잘못 입력하였습니다.",
#     description = "다시 입력해주세요.", color = discord.Color.dark_red()
#     )
#     await ctx.send(embed=embed)
    


@client.command(name="탈퇴")
async def check(ctx):
    try:
        embed = discord.Embed(title = "잠시만 기다려주세요...",
        description = " ", color = discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        try:
            user_id = ctx.author.id
            check = user_check(user_id)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#탈퇴 usercheck부분", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)
        
        if check == 0:
            embed = discord.Embed(title = "탈퇴",
            description = "개인정보 등록이 되어있지 않습니다.", color = discord.Color.dark_gold()
            )
            await ctx.send(embed=embed)

        elif check == 1:
            user_id = ctx.author.id

            con = psycopg2.connect(
                host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                dbname='dc1tl1m2lv0mgi', 
                user='fsnoeuopgcpfpz', 
                password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                port='5432')

            cur = con.cursor()

            cur.execute("DELETE FROM user_info WHERE id = '%s'", (user_id,))

            con.commit()
            cur.close()
            con.close()

            embed = discord.Embed(title = "탈퇴",
            description = "성공적으로 개인정보가 삭제되었습니다.", color = discord.Color.dark_gold()
            )
            await ctx.send(embed=embed)


    except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#탈퇴 부분", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

@client.command(name="ㅌㅌ")
async def check(ctx):
    try:
        embed = discord.Embed(title = "잠시만 기다려주세요...",
        description = " ", color = discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        try:
            user_id = ctx.author.id
            check = user_check(user_id)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#탈퇴 usercheck부분", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)
        
        if check == 0:
            embed = discord.Embed(title = "탈퇴",
            description = "개인정보 등록이 되어있지 않습니다.", color = discord.Color.dark_gold()
            )
            await ctx.send(embed=embed)

        elif check == 1:
            user_id = ctx.author.id

            con = psycopg2.connect(
                host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                dbname='dc1tl1m2lv0mgi', 
                user='fsnoeuopgcpfpz', 
                password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                port='5432')

            cur = con.cursor()

            cur.execute("DELETE FROM user_info WHERE id = '%s'", (user_id,))

            con.commit()
            cur.close()
            con.close()

            embed = discord.Embed(title = "탈퇴",
            description = "성공적으로 개인정보가 삭제되었습니다.", color = discord.Color.dark_gold()
            )
            await ctx.send(embed=embed)


    except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#탈퇴 부분", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

    
@client.command(name="xx")
async def check(ctx):
    try:
        embed = discord.Embed(title = "잠시만 기다려주세요...",
        description = " ", color = discord.Color.blue()
        )
        await ctx.send(embed=embed)
        
        try:
            user_id = ctx.author.id
            check = user_check(user_id)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#탈퇴 usercheck부분", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)
        
        if check == 0:
            embed = discord.Embed(title = "탈퇴",
            description = "개인정보 등록이 되어있지 않습니다.", color = discord.Color.dark_gold()
            )
            await ctx.send(embed=embed)

        elif check == 1:
            user_id = ctx.author.id

            con = psycopg2.connect(
                host='ec2-3-222-127-167.compute-1.amazonaws.com', 
                dbname='dc1tl1m2lv0mgi', 
                user='fsnoeuopgcpfpz', 
                password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
                port='5432')

            cur = con.cursor()

            cur.execute("DELETE FROM user_info WHERE id = '%s'", (user_id,))

            con.commit()
            cur.close()
            con.close()

            embed = discord.Embed(title = "탈퇴",
            description = "성공적으로 개인정보가 삭제되었습니다.", color = discord.Color.dark_gold()
            )
            await ctx.send(embed=embed)


    except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#탈퇴 부분", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)
    

@client.command(name="내정보")
async def check(ctx):
    # if ctx.content == "#내정보":
    user = ctx.author
    await ctx.send(f"이름 : {user.name}\nID : {user.id}")

# ===================================Selenium==========================================
@client.command(name="진단")
async def check(ctx):
    user_id = ctx.author.id
    check = user_check(user_id)

    if check == 0:

        embed = discord.Embed(title = "미가입 유저입니다. #가입 으로 가입해주십시오.",
        color = discord.Color.red()
        )
        await ctx.send(embed=embed)

    elif check == 1:
        user_id = ctx.author.id

        con = psycopg2.connect(
            host='ec2-3-222-127-167.compute-1.amazonaws.com', 
            dbname='dc1tl1m2lv0mgi', 
            user='fsnoeuopgcpfpz', 
            password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
            port='5432')

        cur = con.cursor()

        cur.execute("SELECT * FROM user_info WHERE id = '%s'", (user_id,))
        A_info = cur.fetchall()
        A_info = str(A_info[0]).replace("'", "").replace(',',"").replace('(',"").replace(')',"").split(" ")
        name = A_info[1]
        birth = A_info[2]
        psd = A_info[3]

        con.commit()
        cur.close()
        con.close()


        # if ctx.content == "#진단":
        embed = discord.Embed(title = "실행 중...",
        color = discord.Color.green()
        )
        await ctx.send(embed=embed)



        url = "https://hcs.eduro.go.kr/#/loginHome"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        # driver = webdriver.Chrome('chromedriver.exe')

        driver.get(url)

        driver.find_element_by_xpath('//*[@id="btnConfirm2"]').click() #시작화면에서 시작 버튼 클릭

        time.sleep(1)


        # driver.execute_script("arguments[0].removeAttribute('readonly', 'readonly')", ele)
        # ele.clear()
        # ele.click()

        try:
            # 학교 검색 버튼
            ele = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr[1]/td/button')
            ele.send_keys(Keys.ENTER)
            time.sleep(0.35)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 학교 검색 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 시/도 선택 버튼             
            driver.find_element_by_xpath('//*[@id="sidolabel"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 시/도 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 전라북도 버튼
            driver.find_element_by_xpath('//*[@id="sidolabel"]/option[14]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 전라북도 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #학교급 선택 버튼
            driver.find_element_by_xpath('//*[@id="crseScCode"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교급 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #고등학교 버튼
            driver.find_element_by_xpath('//*[@id="crseScCode"]/option[5]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#고등학교 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 학교 이름 선택 버튼
            schname = driver.find_element_by_xpath('//*[@id="orgname"]') 
            schname.click()
            schname.send_keys("전라고등학교")
            schname.send_keys(Keys.RETURN)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 학교 이름 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        time.sleep(0.5)

        try:
            #학교 선택
            driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a/span').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교 선택", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #학교선택 버튼 클릭
            driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[2]/input').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교선택 버튼 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #이름 입력 칸 클릭
            inputname = driver.find_element_by_xpath('//*[@id="user_name_input"]') 
            inputname.click()
            inputname.send_keys(name)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#이름 입력 칸 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        
        try:
            #생년월일 입력 칸 클릭
            inputdate = driver.find_element_by_xpath('//*[@id="birthday_input"]') 
            inputdate.click()
            inputdate.send_keys(birth)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#생년월일 입력 칸 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)


        try:
            #생년월일 이후 확인 버튼
            driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#생년월일 이후 확인 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)


        time.sleep(3)

        try:
            #비번 입력 칸
            
            inputpsd = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr/td/input')
            inputpsd.click()
            inputpsd.send_keys(psd + Keys.ENTER)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#비번 입력 칸", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        
        # try:
        #     #비번 이후 확인 버튼
        #     psdbtn = driver.find_element_by_css_selector(
        #         "#btnConfirm"
        #     )
        #     psdbtn.send_keys(Keys.ENTER)
        #     send_email(driver)
        #     time.sleep(1)
        # except Exception as ex:            
        #     embed = discord.Embed(title = "Failed",
        #     description = "#비번 이후 확인 버튼", color = discord.Color.red()
        #     )
        #     await ctx.channel.send(embed=embed)
        #     await ctx.channel.send(ex)

        time.sleep(5)

        try:
            #자가진단 버튼
            driver.find_element_by_xpath(
                '//*[@id="container"]/div/section[2]/div[2]/ul/li/a/em'
            ).click()
            # send_email(driver)
            # time.sleep(1)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#자가진단 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        time.sleep(2)


        # ===================================BeautifulSoup==========================================

        try:
            driver.find_element_by_xpath('//*[@id="survey_q1a1"]').click()
            driver.find_element_by_xpath('//*[@id="survey_q2a1"]').click()
            driver.find_element_by_xpath('//*[@id="survey_q3a1"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
            time.sleep(1)
            driver.close()
            
            embed = discord.Embed(title = "Success",
            description = "자가진단이 완료되었습니다.", color = discord.Color.blue()
            )
            await ctx.send(embed=embed) 


        except Exception as ex:
            if '마지막 설문결과 3분후 재설문이 가능합니다.' in str(ex):
                desc = "이미 자가진단이 완료되어있습니다."
            else:
                desc = ex

            embed = discord.Embed(title = "Failed",
            description = desc, color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)
            send_email(driver)

@client.command(name="ㅈㄷ")
async def check(ctx):
    user_id = ctx.author.id
    check = user_check(user_id)

    if check == 0:

        embed = discord.Embed(title = "미가입 유저입니다. #가입 으로 가입해주십시오.",
        color = discord.Color.red()
        )
        await ctx.send(embed=embed)

    elif check == 1:
        user_id = ctx.author.id

        con = psycopg2.connect(
            host='ec2-3-222-127-167.compute-1.amazonaws.com', 
            dbname='dc1tl1m2lv0mgi', 
            user='fsnoeuopgcpfpz', 
            password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
            port='5432')

        cur = con.cursor()

        cur.execute("SELECT * FROM user_info WHERE id = '%s'", (user_id,))
        A_info = cur.fetchall()
        A_info = str(A_info[0]).replace("'", "").replace(',',"").replace('(',"").replace(')',"").split(" ")
        name = A_info[1]
        birth = A_info[2]
        psd = A_info[3]

        con.commit()
        cur.close()
        con.close()


        # if ctx.content == "#진단":
        embed = discord.Embed(title = "실행 중...",
        color = discord.Color.green()
        )
        await ctx.send(embed=embed)



        url = "https://hcs.eduro.go.kr/#/loginHome"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        # driver = webdriver.Chrome('chromedriver.exe')

        driver.get(url)

        driver.find_element_by_xpath('//*[@id="btnConfirm2"]').click() #시작화면에서 시작 버튼 클릭

        time.sleep(1)


        # driver.execute_script("arguments[0].removeAttribute('readonly', 'readonly')", ele)
        # ele.clear()
        # ele.click()

        try:
            # 학교 검색 버튼
            ele = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr[1]/td/button')
            ele.send_keys(Keys.ENTER)
            time.sleep(0.35)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 학교 검색 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 시/도 선택 버튼             
            driver.find_element_by_xpath('//*[@id="sidolabel"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 시/도 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 전라북도 버튼
            driver.find_element_by_xpath('//*[@id="sidolabel"]/option[14]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 전라북도 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #학교급 선택 버튼
            driver.find_element_by_xpath('//*[@id="crseScCode"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교급 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #고등학교 버튼
            driver.find_element_by_xpath('//*[@id="crseScCode"]/option[5]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#고등학교 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 학교 이름 선택 버튼
            schname = driver.find_element_by_xpath('//*[@id="orgname"]') 
            schname.click()
            schname.send_keys("전라고등학교")
            schname.send_keys(Keys.RETURN)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 학교 이름 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        time.sleep(0.5)

        try:
            #학교 선택
            driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a/span').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교 선택", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #학교선택 버튼 클릭
            driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[2]/input').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교선택 버튼 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #이름 입력 칸 클릭
            inputname = driver.find_element_by_xpath('//*[@id="user_name_input"]') 
            inputname.click()
            inputname.send_keys(name)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#이름 입력 칸 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        
        try:
            #생년월일 입력 칸 클릭
            inputdate = driver.find_element_by_xpath('//*[@id="birthday_input"]') 
            inputdate.click()
            inputdate.send_keys(birth)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#생년월일 입력 칸 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)


        try:
            #생년월일 이후 확인 버튼
            driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#생년월일 이후 확인 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)


        time.sleep(3)

        try:
            #비번 입력 칸
            
            inputpsd = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr/td/input')
            inputpsd.click()
            inputpsd.send_keys(psd + Keys.ENTER)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#비번 입력 칸", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        
        # try:
        #     #비번 이후 확인 버튼
        #     psdbtn = driver.find_element_by_css_selector(
        #         "#btnConfirm"
        #     )
        #     psdbtn.send_keys(Keys.ENTER)
        #     send_email(driver)
        #     time.sleep(1)
        # except Exception as ex:            
        #     embed = discord.Embed(title = "Failed",
        #     description = "#비번 이후 확인 버튼", color = discord.Color.red()
        #     )
        #     await ctx.channel.send(embed=embed)
        #     await ctx.channel.send(ex)

        time.sleep(5)

        try:
            #자가진단 버튼
            driver.find_element_by_xpath(
                '//*[@id="container"]/div/section[2]/div[2]/ul/li/a/em'
            ).click()
            # send_email(driver)
            # time.sleep(1)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#자가진단 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        time.sleep(2)


        # ===================================BeautifulSoup==========================================

        try:
            driver.find_element_by_xpath('//*[@id="survey_q1a1"]').click()
            driver.find_element_by_xpath('//*[@id="survey_q2a1"]').click()
            driver.find_element_by_xpath('//*[@id="survey_q3a1"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
            time.sleep(1)
            driver.close()
            
            embed = discord.Embed(title = "Success",
            description = "자가진단이 완료되었습니다.", color = discord.Color.blue()
            )
            await ctx.send(embed=embed) 


        except Exception as ex:
            if '마지막 설문결과 3분후 재설문이 가능합니다.' in str(ex):
                desc = "이미 자가진단이 완료되어있습니다."
            else:
                desc = ex

            embed = discord.Embed(title = "Failed",
            description = desc, color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)
            send_email(driver)

@client.command(name="we")
async def check(ctx):
    user_id = ctx.author.id
    check = user_check(user_id)

    if check == 0:

        embed = discord.Embed(title = "미가입 유저입니다. #가입 으로 가입해주십시오.",
        color = discord.Color.red()
        )
        await ctx.send(embed=embed)

    elif check == 1:
        user_id = ctx.author.id

        con = psycopg2.connect(
            host='ec2-3-222-127-167.compute-1.amazonaws.com', 
            dbname='dc1tl1m2lv0mgi', 
            user='fsnoeuopgcpfpz', 
            password='c4da0044a514dfe06d31fe9c69831d75e46b6f91f11ef53664985a0982ddb8a5', 
            port='5432')

        cur = con.cursor()

        cur.execute("SELECT * FROM user_info WHERE id = '%s'", (user_id,))
        A_info = cur.fetchall()
        A_info = str(A_info[0]).replace("'", "").replace(',',"").replace('(',"").replace(')',"").split(" ")
        name = A_info[1]
        birth = A_info[2]
        psd = A_info[3]

        con.commit()
        cur.close()
        con.close()


        # if ctx.content == "#진단":
        embed = discord.Embed(title = "실행 중...",
        color = discord.Color.green()
        )
        await ctx.send(embed=embed)



        url = "https://hcs.eduro.go.kr/#/loginHome"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        # driver = webdriver.Chrome('chromedriver.exe')

        driver.get(url)

        driver.find_element_by_xpath('//*[@id="btnConfirm2"]').click() #시작화면에서 시작 버튼 클릭

        time.sleep(1)


        # driver.execute_script("arguments[0].removeAttribute('readonly', 'readonly')", ele)
        # ele.clear()
        # ele.click()

        try:
            # 학교 검색 버튼
            ele = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr[1]/td/button')
            ele.send_keys(Keys.ENTER)
            time.sleep(0.35)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 학교 검색 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 시/도 선택 버튼             
            driver.find_element_by_xpath('//*[@id="sidolabel"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 시/도 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 전라북도 버튼
            driver.find_element_by_xpath('//*[@id="sidolabel"]/option[14]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 전라북도 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #학교급 선택 버튼
            driver.find_element_by_xpath('//*[@id="crseScCode"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교급 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #고등학교 버튼
            driver.find_element_by_xpath('//*[@id="crseScCode"]/option[5]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#고등학교 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            # 학교 이름 선택 버튼
            schname = driver.find_element_by_xpath('//*[@id="orgname"]') 
            schname.click()
            schname.send_keys("전라고등학교")
            schname.send_keys(Keys.RETURN)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "# 학교 이름 선택 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        time.sleep(0.5)

        try:
            #학교 선택
            driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a/span').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교 선택", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #학교선택 버튼 클릭
            driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[2]/input').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#학교선택 버튼 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        try:
            #이름 입력 칸 클릭
            inputname = driver.find_element_by_xpath('//*[@id="user_name_input"]') 
            inputname.click()
            inputname.send_keys(name)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#이름 입력 칸 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        
        try:
            #생년월일 입력 칸 클릭
            inputdate = driver.find_element_by_xpath('//*[@id="birthday_input"]') 
            inputdate.click()
            inputdate.send_keys(birth)
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#생년월일 입력 칸 클릭", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)


        try:
            #생년월일 이후 확인 버튼
            driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#생년월일 이후 확인 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)


        time.sleep(3)

        try:
            #비번 입력 칸
            
            inputpsd = driver.find_element_by_xpath('//*[@id="WriteInfoForm"]/table/tbody/tr/td/input')
            inputpsd.click()
            inputpsd.send_keys(psd + Keys.ENTER)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#비번 입력 칸", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        
        # try:
        #     #비번 이후 확인 버튼
        #     psdbtn = driver.find_element_by_css_selector(
        #         "#btnConfirm"
        #     )
        #     psdbtn.send_keys(Keys.ENTER)
        #     send_email(driver)
        #     time.sleep(1)
        # except Exception as ex:            
        #     embed = discord.Embed(title = "Failed",
        #     description = "#비번 이후 확인 버튼", color = discord.Color.red()
        #     )
        #     await ctx.channel.send(embed=embed)
        #     await ctx.channel.send(ex)

        time.sleep(5)

        try:
            #자가진단 버튼
            driver.find_element_by_xpath(
                '//*[@id="container"]/div/section[2]/div[2]/ul/li/a/em'
            ).click()
            # send_email(driver)
            # time.sleep(1)

        except Exception as ex:
            embed = discord.Embed(title = "Failed",
            description = "#자가진단 버튼", color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)

        time.sleep(2)


        # ===================================BeautifulSoup==========================================

        try:
            driver.find_element_by_xpath('//*[@id="survey_q1a1"]').click()
            driver.find_element_by_xpath('//*[@id="survey_q2a1"]').click()
            driver.find_element_by_xpath('//*[@id="survey_q3a1"]').click()
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
            time.sleep(1)
            driver.close()
            
            embed = discord.Embed(title = "Success",
            description = "자가진단이 완료되었습니다.", color = discord.Color.blue()
            )
            await ctx.send(embed=embed) 


        except Exception as ex:
            if '마지막 설문결과 3분후 재설문이 가능합니다.' in str(ex):
                desc = "이미 자가진단이 완료되어있습니다."
            else:
                desc = ex

            embed = discord.Embed(title = "Failed",
            description = desc, color = discord.Color.red()
            )
            await ctx.send(embed=embed)
            await ctx.send(ex)
            send_email(driver)

        
@client.command(name="도움말")
async def meal(ctx):
    embed = discord.Embed(title = "명령어",
    description = "전라고등학교 자가진단 봇 명령어" , color = 0xE66389
    )

    embed.add_field(name="#가입 \n#ㄱㅇ \n#rd", value="자가진단 봇 서비스에 가입합니다.\n※사용법 : #가입 (이름) (생년월일) (비밀번호)\nex)이름 : 백민혁, 생년월일: 2003.08.05, 자가진단 사이트 비밀번호 :1234 인 경우 \n#가입 백민혁 030805 1234", inline=False)
    embed.add_field(name="#탈퇴 \n#ㄱㅇ \n#xx", value="자가진단 봇 서비스에서 자신의 개인정보를 삭제하여 탈퇴합니다.", inline=False)
    embed.add_field(name="#진단 \n#ㅈㄷ \n#we", value="자가진단 사이트에서 자가진단을 실시해줍니다. \n최소 10초 ~ 1분 정도의 시간이 소요됩니다.", inline=False)
    
    await ctx.send(embed=embed)

@client.command(name="명령어")
async def meal(ctx):
    embed = discord.Embed(title = "명령어",
    description = "전라고등학교 자가진단 봇 명령어" , color = 0xE66389
    )

    embed.add_field(name="#가입 \n#ㄱㅇ \n#rd", value="자가진단 봇 서비스에 가입합니다.\n※사용법 : #가입 (이름) (생년월일) (비밀번호)\nex)이름 : 백민혁, 생년월일: 2003.08.05, 자가진단 사이트 비밀번호 :1234 인 경우 \n#가입 백민혁 030805 1234", inline=False)
    embed.add_field(name="#탈퇴 \n#ㄱㅇ \n#xx", value="자가진단 봇 서비스에서 자신의 개인정보를 삭제하여 탈퇴합니다.", inline=False)
    embed.add_field(name="#진단 \n#ㅈㄷ \n#we", value="자가진단 사이트에서 자가진단을 실시해줍니다. \n최소 10초 ~ 1분 정도의 시간이 소요됩니다.", inline=False)
    
    await ctx.send(embed=embed)

client.remove_command("help")
@client.command(name="help")
async def meal(ctx):
    embed = discord.Embed(title = "명령어",
    description = "전라고등학교 자가진단 봇 명령어" , color = 0xE66389
    )

    embed.add_field(name="#가입 \n#ㄱㅇ \n#rd", value="자가진단 봇 서비스에 가입합니다.\n※사용법 : #가입 (이름) (생년월일) (비밀번호)\nex)이름 : 백민혁, 생년월일: 2003.08.05, 자가진단 사이트 비밀번호 :1234 인 경우 \n#가입 백민혁 030805 1234", inline=False)
    embed.add_field(name="#탈퇴 \n#ㄱㅇ \n#xx", value="자가진단 봇 서비스에서 자신의 개인정보를 삭제하여 탈퇴합니다.", inline=False)
    embed.add_field(name="#진단 \n#ㅈㄷ \n#we", value="자가진단 사이트에서 자가진단을 실시해줍니다. \n최소 10초 ~ 1분 정도의 시간이 소요됩니다.", inline=False)
    
    await ctx.send(embed=embed)

@client.command(name="?")
async def meal(ctx):
    embed = discord.Embed(title = "명령어",
    description = "전라고등학교 자가진단 봇 명령어" , color = 0xE66389
    )

    embed.add_field(name="#가입 \n#ㄱㅇ \n#rd", value="자가진단 봇 서비스에 가입합니다.\n※사용법 : #가입 (이름) (생년월일) (비밀번호)\nex)이름 : 백민혁, 생년월일: 2003.08.05, 자가진단 사이트 비밀번호 :1234 인 경우 \n#가입 백민혁 030805 1234", inline=False)
    embed.add_field(name="#탈퇴 \n#ㄱㅇ \n#xx", value="자가진단 봇 서비스에서 자신의 개인정보를 삭제하여 탈퇴합니다.", inline=False)
    embed.add_field(name="#진단 \n#ㅈㄷ \n#we", value="자가진단 사이트에서 자가진단을 실시해줍니다. \n최소 10초 ~ 1분 정도의 시간이 소요됩니다.", inline=False)
    
    await ctx.send(embed=embed)
    
@client.command(name="command")
async def meal(ctx):
    embed = discord.Embed(title = "명령어",
    description = "전라고등학교 자가진단 봇 명령어" , color = 0xE66389
    )

    embed.add_field(name="#가입 \n#ㄱㅇ \n#rd", value="자가진단 봇 서비스에 가입합니다.\n※사용법 : #가입 (이름) (생년월일) (비밀번호)\nex)이름 : 백민혁, 생년월일: 2003.08.05, 자가진단 사이트 비밀번호 :1234 인 경우 \n#가입 백민혁 030805 1234", inline=False)
    embed.add_field(name="#탈퇴 \n#ㄱㅇ \n#xx", value="자가진단 봇 서비스에서 자신의 개인정보를 삭제하여 탈퇴합니다.", inline=False)
    embed.add_field(name="#진단 \n#ㅈㄷ \n#we", value="자가진단 사이트에서 자가진단을 실시해줍니다. \n최소 10초 ~ 1분 정도의 시간이 소요됩니다.", inline=False)
    
    await ctx.send(embed=embed)


client.run(os.environ['token'])
# client.run("ODE0MzExODc5MzA3NTU4OTQy.
# YDcBCQ.mM629IJgb7mwbWqDWbwKW_KIwxE")
