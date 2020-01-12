#!/usr/bin/python3

from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import subprocess
import telebot
from urllib.parse import unquote
import youtube_dl
from telethon import TelegramClient, events, sync
import datetime


# Parameters
bot_token = '#BOT_TOKEN'
chat_id = "#CHAT_ID"
url = "https://www.dw.com/es/multimedia/todos-los-contenidos/s-100838?filter=&type=18&programs=262016&period=day&sort=date&results=16"
# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 0000000
api_hash = '00000000000000000000000000000000'

bot = telebot.TeleBot(bot_token)

# Print date to log for better debugging
print (datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S"))

# Getting the webpage, creating a Response object.
response = requests.get(url)
 
# Extracting the source code of the page.
data = response.text
 
# Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
soup = BeautifulSoup(data, 'lxml')
 
# Extracting all the <a> tags into a list.
tags = soup.find_all('a')
 
# Extracting URLs from the attribute href in the <a> tags.
for tag in tags:
    cadena=tag.get('href')
    if "hora" in str(cadena):
        fincadena=tag.get('href')


url = "https://www.dw.com"+fincadena

#subprocess.run(["youtube-dl", url, "-o", "video.mp4"])
#Using python youtube_dl rather than command

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    video=ydl.extract_info(url)

url_string = video['url']
id_video = url_string[56:72]
video_filename = "videos/"+id_video+".mp4"
video_metadata = "videos/"+id_video+".metadata"
f=open(video_metadata, "a+")
f.write(str(video))
url_m3u8= "https://dwhlsondemand-vh.akamaihd.net/i/dwtv_video/flv/kuns/"+id_video+"_sd_,sor,avc,.mp4.csmil/index_1_av.m3u8?null=0"

try:
    with open(video_filename, 'r') as fh:
        print("Nothing to do here")
except FileNotFoundError:
    # Keep preset values
    # https://raw.githubusercontent.com/lcy0321/m3u8-downloader/master/m3u8_downloader.py
    subprocess.run(["./m3u8_downloader.py","-o", video_filename, url_m3u8])
    
    chat_id= 'dw_noticias'
    client = TelegramClient('session_name', api_id, api_hash)
    client.start()
    
    print(client.get_me().stringify())
    
    client.send_file(chat_id, video_filename, supports_streaming=True)
    
    client.disconnect()
    
