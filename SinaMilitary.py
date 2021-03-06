# -*- coding: utf8 -*-
import re
import requests
import codecs
import time
import random
from bs4 import BeautifulSoup
import sys
stdout = sys.stdout
reload(sys)
sys.stdout = stdout
sys.setdefaultencoding('utf8')

url_Base = "http://roll.mil.news.sina.com.cn/col/zgjq"
url_First_Page = "http://roll.mil.news.sina.com.cn/col/zgjq/index.shtml"  # 新浪军事——中国军情（第1页）

next = []
User_Agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3368.400 QQBrowser/9.6.11860.400',
              'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko']

def get_NewsContent(News_Html, News_Title, News_Date, output):
    userAgent = random.choice(User_Agent)
    header = {'User-Agent': userAgent, 'Connection': 'keep-alive'}
    html = requests.get(News_Html, headers=header).content  # 请求页面内容
    soup = BeautifulSoup(html, 'lxml')
    paragraph = []
    paragraph = soup.select('div[class="article"] > p')   # 以自然段为单位
    output.writelines(News_Date[1:-1] + "\t" + News_Title + "\n")
    if(len(paragraph) == 0):
        paragraph = soup.select('div[class="content"] > p')
    for i in range(0,len(paragraph)):
        if((paragraph[i].text != "\n") and (paragraph[i].text != " ")):
            content = paragraph[i].text.strip()
            output.writelines(content + "\n")
    output.writelines("****************************\n")

def get_NewsInThisPage(url, output):
    userAgent = random.choice(User_Agent)
    header = {'User-Agent': userAgent, 'Connection': 'keep-alive'}
    html = requests.get(url, headers=header).content  # 请求页面内容
    soup = BeautifulSoup(html, 'lxml')
    NewsTitle = soup.select('ul[class="linkNews"] > li > a')
    NewsDate = soup.select('ul[class="linkNews"] > li > span')
    for i in range(0,len(NewsTitle)):
        News_Html = NewsTitle[i].get('href')
        News_Title = NewsTitle[i].text
        News_Date = NewsDate[i].text
        get_NewsContent(News_Html, News_Title, News_Date, output)
    # 下一页的链接
    next = soup.select('span[class="pagebox_next"] > a')
    return next

def get_News():
    url = url_First_Page
    flag = 0
    firstFlag = True
    next_page = ""
    page = 1
    output = open("SinaNews_Ori.txt", "w")
    while(flag != 1):
        print "第 " + str(page) + " 页"
        output.writelines("-----------------第 " + str(page) + " 页" + "\n")
        if(firstFlag):
            firstFlag = False
        else:
            url = url_Base + next_page
        next = get_NewsInThisPage(url, output)
        if(len(next) == 0):
            flag = 1
        else:
            next_page = next[0].get('href')[1:]
            page += 1
        if(page > 10):
            print "OK!"
            output.close()
            break
        time.sleep(1 + float(random.randint(1, 100)) / 20)

if __name__ == '__main__':
    get_News()