# _*_encoding:utf-8 _*_
"""
@Softwave: Pycharm
@Python: 3.X
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.10.30
"""

import requests
from bs4 import BeautifulSoup
from lxml import html
import time

# 两者大致相同，只是所抓取数据部分不同，
class huxiu_article():

    def __init__(self):
        self.name = "huxiu"
        self.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    }
        self.huxiu_url = "https://www.huxiu.com"


    def get_url(self):
        response = requests.get(url=self.huxiu_url, headers=self.headers, verify=True)

        # print(response.text)

        soup = BeautifulSoup(response.text, 'lxml')
        # 获取所有的a标签
        info = soup.find_all('a')

        url_all = []

        for a in info:

            try:   # 筛选带有article的url，也就是过滤其他非文章url
                if 'article' == a['href'][1:8:1]:

                    # print(a['href'])

                    url_all.append(a['href'])

            except KeyError:
                pass

        return set(url_all)
    # 保存抓取的数据部分
    def save_info(self,info):

        file_name = self.name + str(time.strftime("%Y-%m-%d", time.localtime())) + '.txt'

        with open(file_name, 'a+', encoding='utf-8') as f:

            f.writelines(info)

            f.write('\n\n')

    def get_info(self):
        URL = self.get_url()
        for url in URL:       #文章的xpath部分随文章的不同而不同。需要自己构造
            id_str = url[9:15:1]

            article_url = self.huxiu_url + url

            # print(url)

            res = requests.get(url=article_url, headers=self.headers, verify=True)

            selector = html.fromstring(res.text)
            # 获取所需要的数据
            try:
                title = selector.xpath('//*[@id="article' + id_str + '"]/div[2]/div[2]/h1/text()')[0].strip()

                author = selector.xpath('//*[@id="article' + id_str + '"]/div[3]/div[1]/div[2]/a[1]/text()')[0].strip()

                time = selector.xpath('//*[@id="article' + id_str + '"]/div[2]/div[2]/div[1]/div/span[1]/text()')[
                    0].strip()

                img_url = selector.xpath('//*[@id="article' + id_str + '"]/div[2]/div[2]//img/@src')[0].strip()

                # print(title, author, time, img_url)

                info = [title, author, time, article_url, img_url]

                print(info)

                self.save_info(info=info)

            except IndexError:
                print('url= {}出现点错误'.format(url))
# 与上面大致相同，思路是一样的
class leifeng_article():

    def __init__(self):
        self.name = 'leifeng'
        self.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
    }
        self.leifeng = "https://www.leiphone.com/"


    def get_url(self):
        response = requests.get(url=self.leifeng, headers=self.headers, verify=True)

        # print(response.text)

        soup = BeautifulSoup(response.text, 'lxml')

        info = soup.find_all('a')

        url_all = []

        for a in info:

            try:

                if 'news' == a['href'][25:29:1]:
                    print(a['href'])

                    url_all.append(a['href'])

            except KeyError:
                pass

        return set(url_all)

    def save_info(self,info):

        file_name = self.name + str(time.strftime("%Y-%m-%d", time.localtime())) + '.txt'

        with open(file_name, 'a+', encoding='utf-8') as f:

            f.writelines(info)

            f.write('\n\n')

    def get_info(self):
        URL = self.get_url()
        for article_url in URL:

            res = requests.get(url=article_url, headers=self.headers, verify=True)

            selector = html.fromstring(res.text)

            try:
                title = selector.xpath('/html/body/div[5]/div[1]/div[1]/div/h1/text()')[0].strip()

                author = selector.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/table//tr/td[1]/a/text()')[
                    0].strip()

                time = selector.xpath('/html/body/div[5]/div[1]/div[1]/div/div[1]/table//tr/td[2]/text()')[0].strip()

                img_url = selector.xpath('/html/body/div[5]/div[1]/div[2]/div/div[1]/div[1]//img/@src')[0].strip()

                # print(title, author, time, img_url)

                info = [title, author, time, article_url, img_url]

                print(info)

                self.save_info(info=info)

            except IndexError:
                print('url= {}出现点错误'.format(article_url))
if __name__ == '__main__':
    huxiu = huxiu_article()
    huxiu.get_info()

    leifeng = leifeng_article()
    leifeng.get_info()
