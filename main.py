#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.11.22
"""
import sys

import requests

import time

import random

from autoSendBlog import autoSendBlog

from sendEmail import sendmail

from spider.huxiu import huxiu

from spider.kr import kr

from spider.tmtpost import tmtpost

from spider.leiphone import leiphone

from Socket_Client import Socket_Send

from News_DB import write_db, read_db

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
        self.post_url = "http://123.206.254.253/Cetus/Public/cetus/"
        # 用来记录一天的发送记录。
        self.content = ""

    # 获取当前系统的时间，类型为：str
    def time_now(self):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return time_now

    def autoSendBolg(self, news):
        blog = autoSendBlog()
        flag = blog.SendBlog(news)
        if flag == 1:
            print(self.time_now(), '\tGood, Blog is send success! @SKYNE\n')
        else:
            print(self.time_now(), '\tBlog seng error! please check the error = {}! @SKYNE\n'.format(flag))
            content = 'Blog seng error! please check the error is that ' + flag + '@SKYNE\n'
            sendmail(content)


    # 使用post的方法，发送抓取信息至指定API接口。
    def post_data(self, news):
        res = requests.post(url= self.post_url, data= news, headers= self.headers)
        if res.status_code == 200:
            print(self.time_now(), "\tGood,Send success @SKYNE url=" + news['link'] + "\n")
            self.content = self.content + self.time_now() + "\tGood,Send success" + news['link'] + "<br>"

    def get_url(self):
        hu = huxiu()
        tmt = tmtpost()
        k = kr()
        url_list = hu.get_url() + tmt.get_url() + k.get_url()
        # print(url_list)
        return url_list

    def get_news(self, url):
        """
        :param url: 需要抓取内容的URL地址
        :url[12]: 判断对应的url，h, m, 3, l分别对应：huxiu, tmtpost, 36kr, leiphone
        :return: news
        """
        if url:
            if url[12] == 'h':
                hu = huxiu()
                return hu.get_news(url=url)

            elif url[12] == 'm':
                tmt = tmtpost()
                return tmt.get_news(url= url)

            elif url[9] == 'k' or url[10] == 'k':
                k = kr()
                return k.get_news(url= url)
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

    def main(self):
        print(self.time_now(),'\tProgram is starting up! please waiting! @SKYNE\n')
        hour_counter = 0
        url_queue = queue()
        url_new = self.get_url()
        url_queue = self.random_url(queue= url_queue, url_list= url_new)
        while(True):
            if hour_counter % 4 == 0:
                print(self.time_now(), '\tThe program is performing {} queries ! @SKYNE\n'.format(hour_counter))

            flag = True
            while (flag):
                if url_queue.is_empty():
                    print (self.time_now (), '\tThe queue is empty @SKYNE\n')
                    flag = False
                else:
                    news = self.get_news(url= url_queue.dequeue())
                    if news:
                        if write_db(news):
                            flag = False

                            
            if time.localtime()[3] %3 == 0:
                news = read_db()
                self.post_data(news)
                self.autoSendBolg(news)
                Socket_Send(news)


            hour_counter += 1
            time.sleep(1800)

            # 每过两个小时重新查询有无新的url
            if time.localtime()[3] %2 == 0:
                url_old = url_new
                url_new = self.set_url(url_new= self.get_url(), url_old= url_old)
                url_queue = self.random_url(queue= url_queue, url_list= url_new)
                url_new = list(set(url_old + url_new))

            # # print('queue=', url_queue.return_all())
            # # 夜间进入休眠
            # if time.localtime()[3] >= 21:
            #     day_counter += 1
            #     print(self.time_now(), '\tPaogarm delay ten hours! Good night! @SKYNE\n')
            #     mail_header = "Good night SKYNE, The program runs well, and Here is the log! <br>"
            #     sendmail(mail_header + self.content)
            #     self.content = " "
            #     Flag = True
            #     while(Flag):
            #         if time.localtime()[3] == 8:
            #             if day_counter % 2 == 0:
            #                 print(self.time_now(), 'Program is starting up! please waiting! Good morning @SKYNE\n')
            #                 hour_counter = 0
            #                 day_counter = 0
            #                 url_queue = queue()
            #                 url_new = self.get_url()
            #                 url_queue = self.random_url(queue=url_queue, url_list=url_new)
            #                 Flag = False
            #             else:
            #                 Flag = False
            #         else:
            #             time.sleep(1200)



if __name__ == '__main__':
    progarm = progarm()
    progarm.main()