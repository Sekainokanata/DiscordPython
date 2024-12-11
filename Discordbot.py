import discord
#import random
import datetime
#import requests
import subprocess
#import aiohttp
import logging

# ロギングの基本設定
logging.basicConfig(
    level=logging.INFO,  # ログレベルを設定（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),  # ログをファイルに保存
        logging.StreamHandler()          # コンソールにもログを出力
    ]
)

#logger = logging.getLogger('discord')
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
calendar_data = datetime.date.today()#日付確認用
command = ["$today?","$ping","$help","$Good？","$tracert"]#コマンドリスト

FLAG = True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global FLAG
    def pred(m):
        return m.author == message.author and m.channel == message.channel

    if message.author == client.user:
        return
    
    if message.content == command[0]:
        embed = discord.Embed(title="今日の日付",description=str(calendar_data))
        await message.channel.send(embed=embed)

    elif message.content == command[1]:
        FLAG = False
        await message.channel.send('please type IP-address or FQDN...')
        User_IP = await client.wait_for('message', check=pred)
        await message.channel.send('Now running...')
        try:
            result = (subprocess.check_output(["ping", User_IP.content],stderr=subprocess.STDOUT,shell=True))
            await message.channel.send(result.decode('cp932'))
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            output = e.output.decode('cp932')
            await message.channel.send( "Code{},{}".format(returncode,output))

    elif message.content == command[2]:
        await message.channel.send('--------コマンド一覧--------')
        for i in command:
            await message.channel.send(i)
        await message.channel.send('また、コマンドのバグを発見次第、報告願います。')

    elif message.content == command[3]:
        await message.channel.send('元気だよ！')
    
    elif message.content == command[4]:
        FLAG = False
        await message.channel.send('please type IP-address or FQDN...')
        User_IP = await client.wait_for('message', check=pred)
        await message.channel.send('Now running...')
        try:
            result = (subprocess.check_output(["tracert", User_IP.content],stderr=subprocess.STDOUT,shell=True))
            await message.channel.send(result.decode('cp932'))
        except subprocess.CalledProcessError as e:
            returncode = e.returncode
            output = e.output.decode('cp932')
            await message.channel.send( "Code{},{}".format(returncode,output))
    
    else:
        if FLAG:
            await message.channel.send('コマンドが違います。$helpで確認してください。')

try:
    f = open('client.txt', 'r')
    client.run(f.read())
except FileNotFoundError:
    print("Error: 'client.txt' file not found. Please ensure the file exists.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if 'f' in locals() and not f.closed:
        f.close()