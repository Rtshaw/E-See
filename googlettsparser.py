# -*- coding: utf-8 -*-

import os
import requests

def getContent():
    # 讀 output.txt
    with open('output.txt', encoding = 'utf-8-sig') as f:
        content = f.read().strip()
        content = content.replace('________________', '')
        # print(content)
        return content

def getMP3(url):
    s = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja;q=0.6,zh-CN;q=0.5',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'x-client-data': 'CIm2yQEIorbJAQjEtskBCKmdygEIp5/KAQioo8oBGIGYygE=',
    }
    # google 語音
    mp3link = url
    r = s.get(mp3link)
        
    # download mp3 file
    with open('./voice/sample0.mp3', 'wb') as f:
        f.write(r.content)
  
  
