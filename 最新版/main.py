#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.11.22
"""

import requests

import time

from spider import spiders

from article_url import remove_repeat, isExists

from pysql import write

from param import param

from sendmail import sendmail



# 获取当前系统的时间，类型为：str
def time_now():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return time_now


# 使用post的方法，发送抓取信息至指定API接口。
def post_data(news):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0",
    "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36", }
    post_url = "*********************************************"

    news['link'] = news['url']
    news['labels'] = news['author']
    news['service'] = 'Article.AddArticle'
    news[ 'text' ] = ""
    res = requests.post(url= post_url, data= news, headers= headers, verify=False)
    if res.status_code == 200:
        print(time_now(), "\tGood,Send success @SKYNE url=" + news['link'] + "\n")
    else:
        print(time_now(), "\tOh My God,Send Failes @SKYNE url={}\tStatus_code ={}".format(news['link'], res.status_code))



def main():
    names = ['huxiu', 'tmtpost', 'woshipm', 'zaodu', 'pmtoo', 'chanpin']
    content="The task is completed and the system is automatically withdrawn! @SKYNE \n Totalling the following information \n"

    urlSet = []
    for name in names:
        spider = spiders(param[name])
        urlSet = spider.get_url()

        for url in urlSet:
            if remove_repeat(url):
                news=spider.get_news(url)
                if news:
                    write(news)
                    post_data(news)
                    content = content + '\n' + news['title'] + '\n' + news['url'] + '\n' + news['content']
                    time.sleep(1)

    if len(content) > 120:
        print(content)
        sendmail(content, '520@skyne.cn')
        sendmail(content, '1127218124@qq.com')

if __name__ == '__main__':
    main()
