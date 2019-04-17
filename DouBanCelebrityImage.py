# -*- coding: utf-8 -*-
"""
DouBanCelebrityImage.py
从豆瓣影人图片页面下载图片

在 if __name__ == "__main__": 里修改 celebrity_id, 然后运行此文件.
celebrity_id: 影人的豆瓣id, 以赵丽颖为例, 她的豆瓣页面为: https://movie.douban.com/celebrity/1275620/, 影人id就是: 1275620

默认下载前11页的图片, 一般共330张. 可在 main() 函数中修改 download_all_images() 语句中的参数修改下载范围.
"""
import requests, bs4, re
import pandas as pd
import random
import os
import concurrent
from concurrent.futures import ThreadPoolExecutor
from collections import deque
import sys, time

global celebrity_id

if __name__ == "__main__":
    #[x] Dilraba 1325127
    # Mi Yang 1052359
    # Xiaotong Guan 1276032
    #[x] Liya Tong 1275756
    # Xueying Zhang 1326897
    celebrity_id = "1326897"
    main()

my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
]

def dlp(p):
    url = "https://movie.douban.com/celebrity/"+str(celebrity_id)+"/photos/?type=C&start="+str(p*30)+"&sortby=like&size=a&subtype=a"
    req = requests.get(url)
    if req.status_code != 200:
        print("NETWORK ERROR")
        return 1
    content = req.text
    covers = bs4.BeautifulSoup(content, "html.parser", parse_only=bs4.SoupStrainer(class_="cover")).find_all("a")
    img_id = [cover["href"].split("/")[-2] for cover in covers]
    if len(img_id) == 0:
        print("No image in page #%s, please check!" % (str(p)))
        return 1
    img_link = ["https://img3.doubanio.com/view/photo/raw/public/p"+str(id)+".jpg" for id in img_id]
    print("========================= START Page %d: =========================" % p)
    for im,l in zip(img_id, img_link):
        img_dl(l, im)
    print("========================= FINISH Page %d: =========================" % p)

def img_dl(link, filename=""):
    header = {'User-Agent': random.choice(my_headers),"authority": "img3.doubanio.com", "method": "GET", 
              "path": "/view/photo/raw/public/"+link.split("/")[-1], "scheme": "https", "cache-control": "max-age=0",
              "cookie": "bid=cTXrClHCyGw", "referer": "https://movie.douban.com/celebrity/"+str(celebrity_id)+"/photo/"+str(filename)+"/",
              "upgrade-insecure-requests": "1"}
    if len(filename)==0:
        filename = '%s' % (link.split("/")[-1])
    else:
        filename = filename+".jpg"
    with open(filename, 'wb') as f:
        req = requests.get(link, headers=header)
        if req.status_code != 200:
            print("!%s" % filename)
        else:
            f.write(req.content)
            # print(filename, end="  ")

def download_all_images(lr, ur):
    page_range = [i for i in range(lr, ur+1)]
    works = len(page_range)
    with concurrent.futures.ThreadPoolExecutor(works) as exector:
        for p in page_range:
            exector.submit(dlp, p) 

def main():
    url = "https://movie.douban.com/celebrity/"+str(celebrity_id)+"/photos/?type=C&start="+str(0)+"&sortby=like&size=a&subtype=a"
    celebrity_name = bs4.BeautifulSoup(requests.get(url).text, "html.parser").find("h1").text
    print("即将下载的是 %s"%celebrity_name)
    while(True):
        choice = input("Y/N?")
        if choice == "N":
            exit(0)
        elif choice == "Y":
            download_all_images(0, 10)
            exit(0)
        else:
            print("输入有误, 请重新输入")
    print("========================= FINISH ALL =========================")

