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

import re

import random

from spider.huxiu import huxiu

from spider.tmtpost import tmtpost

from spider.zaodu import zaodu

from spider.chanpin import chanpin

from spider.pmtoo import pmtoo

from spider.woshipm import woshipm

from Write_Db import write

import json

# 队列，用以实现抓取的url队列化，先进先出（FIFO）
class queue(object):

    def __init__(self):
        self.items = []

    def is_empty(self):
        return  self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            return  self.items.pop()

    def size(self):
        return len(self.items)

    def is_exist(self, item):
        return item in self.items

    def return_all(self):
        return self.items



class progarm(object):
    def __init__(self):
        self.headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0",
        "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36", }
        self.post_url = "************************************************"

    # 获取当前系统的时间，类型为：str
    def time_now(self):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return time_now


    # 使用post的方法，发送抓取信息至指定API接口。
    def post_data(self, news):

        news['link'] = news['url']
        news['labels'] = news['author']
        news['service'] = 'Article.AddArticle'
        news[ 'text' ] = ""
        res = requests.post(url= self.post_url, data= news, headers= self.headers)
        if res.status_code == 200:
            print(self.time_now(), "\tGood,Send success @SKYNE url=" + news['link'] + "\n")


        # # while语句  去除文本中的![](image_url)markdown形式的图片链接
        # flag = True
        # while (flag):
        #     if -1 == title.find ('!'):
        #         flag = False
        #     else:sss
        #         if -1 == title.find (')'):
        #             title = title[0: title.find ('!') - 1: 1]
        #         else:
        #             title = title[0: title.find ('!') - 1: 1] + title[title.find (')') + 1: -1: 1]

        # 去除文本中的![](image_url)markdown形式的图片链接
        # 终于找到完美匹配的正则表达式  \!\[\]\((https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\)
        # news[ 'content' ] = re.sub("\!\[\]\((https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\)", "", title)   + ".........READMORE"

        ##### 去除段落末尾的不完整段落  ######
        # content = re.sub("\!\[\]\((https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\)", "", news['text'][0:500:1]) \
        #     .replace('/n/n/n', '/n/n').replace('/n/n/n/n', '/n/n').replace('/n/n/n/n/n', '/n/n').replace(
        #     '/n/n/n/n/n/n', '/n/n')
        # point = None
        # for i in range(1,len(content)):
        #     if content[-i] == '/n':
        #         point = len(content) - i + 1
        #         break
        #
        # if point:
        #     news[ 'content' ] = content[0: point :1]
        # else:
        #     news[ 'content' ] = content
        #
        # print(content)


    def get_url(self):
        hu = huxiu()
        tmt = tmtpost()
        zao = zaodu()
        chan = chanpin()
        pmt = pmtoo()
        woshi = woshipm()
        url_list = hu.get_url() + tmt.get_url() + zao.get_url() \
        + chan.get_url() + pmt.get_url() + woshi.get_url()
        # print(url_list)
        return url_list

    def get_news(self, url):
        """
        :param url: 需要抓取内容的URL地址
        :url[12]: 判断对应的url，h, m, 3, l分别对应：huxiu, tmtpost, 36kr, leiphone
        :return: news
        """
        if url:
            if url[11] == 'c':
                chan = chanpin ()
                return chan.get_news (url)

            elif url[12] == 'h':
                hu = huxiu ()
                return hu.get_news (url)

            elif url[11] == 'p':
                pmt = pmtoo ()
                return pmt.get_news(url)

            elif url[12] == 'm':
                tmt = tmtpost()
                return tmt.get_news(url)

            elif url[12] == 'z':
                zao = zaodu()
                return zao.get_news(url)

            elif url[12] == 'o':
                woshi = woshipm ()
                return woshi.get_news(url)

            else:
                print (self.time_now (), '\tAppear error url=', url, '\n')
                return None
        else:
            print(self.time_now(),'\tAppear error url= None\n')
            return None

    # 去除重复的URL地址，返回新增的URL地址
    # print(url in url_old)
    # print(url not in url_old)
    def set_url(self, url_new, url_old):
        url_list = []
        for url in url_new:
            if url not in url_old:
                url_list.append(url)
        return url_list


    # 将获取的url列表中的url随机储存至队列尾部
    """
    :param
    queue: class queue
    url_list: list
    random.sample(): return list
    """
    # 此处自己给自己挖了坑，由于是把列表传进来了，这跟python语法有关，类比c的指针。
    # 并且remove了元素，导致135行之后的url_new已经变成了空列表。0.0
    def random_url(self, queue, url_list):
        if url_list:
            url_tmp = []
            for url in url_list:
                url_tmp.append(url)

            while(url_tmp):
                url = random.sample(url_tmp, 1)
                if len(url[0]) <= 50:
                    queue.enqueue(item= url[0])
                    print(self.time_now(), '\tNew url insert queue success! url={} @SKYNE\n'.format(url[0]))
                    url_tmp.remove(url[0])
                else:
                    url_tmp.remove (url[0])
            return queue
        else:
            print(self.time_now(), '\tNo new url need to insert! @SKYNE\n')
            return queue

    def test_log(self):
        url_queue = queue()
        url_new = self.get_url()
        url_queue = self.random_url(queue= url_queue, url_list= url_new)
        flag = True
        while (flag):
            if url_queue.is_empty ():
                print (self.time_now (), '\tThe queue is empty @SKYNE\n')
                flag = False
            else:
                news = self.get_news (url=url_queue.dequeue ())
                if news:
                    with open ('log.txt', 'a+') as fb:
                        news = json.dumps(news).encode ('utf-8')
                        news = str(json.loads(news.decode('utf-8')))
                        fb.writelines (self.time_now() + "\t" + news  + "\n")
                else:
                    flag = False

    def main(self):
        print(self.time_now(),'\tProgram is starting up! please waiting! @SKYNE\n')
        hour_counter = 0
        url_queue = queue()
        url_new = self.get_url()
        url_queue = self.random_url(queue= url_queue, url_list= url_new)
        while(True):
            if hour_counter % 4 == 0:
                print(self.time_now(), '\tThe program is performing {} queries ! @SKYNE\n'.format(hour_counter * 4))

            flag = True
            while (flag):
                if url_queue.is_empty():
                    print (self.time_now (), '\tThe queue is empty @SKYNE\n')
                    flag = False
                else:
                    news = self.get_news(url= url_queue.dequeue())
                    if news:
                       if write(news):  ##  write() return True or False
                            self.post_data(news)
                            flag = False


            time.sleep(1800)
            hour_counter += 1
            url_old = url_new
            url_new = self.set_url(url_new= self.get_url(), url_old= url_old)
            url_queue = self.random_url(queue= url_queue, url_list= url_new)
            url_new = list(set(url_old + url_new))



if __name__ == '__main__':
    progarm = progarm()
    progarm.main()
    # progarm.test_log()