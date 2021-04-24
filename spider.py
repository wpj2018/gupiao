#coding:utf-8
from selenium import webdriver
import os
import chardet
import time
import sys
import codecs
import threading
import redis
import datetime
from os import listdir
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import urllib
import urllib.request
import re
import os


# 爬虫抓取网页函数
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('utf-8')
    return html

dic = {"shang": "0", "shen": "1", "chuang":"1"}

def redis_connect():
    re = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    return re


def spider(code, code_type):
    start_date="2020"
    url="http://quotes.money.163.com/trade/lsjysj_zhishu_{}.html".format(code)
    download_url = "http://quotes.money.163.com/service/chddata.html?code=" + code_type + code + "&start=" + start_date + "&end=" + end_date + "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"

    path = "csv/" + code + ".csv"
    urllib.request.urlretrieve(download_url, path)
    '''
    start_date = driver.find_element_by_xpath("//*[@name='date_start_value']").get_attribute('value').replace('-','')
    end_date = driver.find_element_by_xpath("//*[@name='date_end_value']").get_attribute('value').replace('-','')
    download_url = "http://quotes.money.163.com/service/chddata.html?code=" + code_type + code + "&start=" + start_date + "&end=" + end_date + "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP"
    driver.get(download_url)
    path = "csv/"+code+".csv"
    #print(start_date, end_date)
    while not os.path.exists(path):
        time.sleep(1)
    print("download {} success".format(code))
    driver.close()
    '''

def spider_thread(code_lst, code_type):
    for code in code_lst:
        spider(code, dic[code_type])


def spider_threads(code_type):
    files = listdir("csv_old")
    exist = {}
    for i in range(len(files)):
        exist[files[i]] = 1

    codes_list = []
    for i in range(40):
        codes_list.append([])
    cnt = 0
    thread_num = 10
    for line in open("resource/{}.txt".format(code_type), encoding="utf-8"):
        if len(line) == 0:
            continue
        code, name = line.split("\t")
        if "{}.csv".format(code) in exist:
            print("{} already exist".format(code))
            continue
        codes_list[cnt].append(code)
        cnt = (cnt + 1) % thread_num

    for i in range(thread_num):
        t = threading.Thread(target=spider_thread,args=(codes_list[i], code_type))
        t.start()


#spider_threads("shang")
#spider_threads("shen")
#spider_threads("chuang")
spider("000300", "shang")
print("success")