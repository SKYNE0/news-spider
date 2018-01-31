# _*_encoding:utf-8_*_
"""
@Python -V: 3.X
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.1.14
"""

import requests

from lxml import html


class chanpin(object):
    def __init__(self):
        self.url = 'http://www.chanpin100.com/pm'
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0",
            "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36", }
        self.session = requests.session()

    def parser(self, url):
        """
        :param url: 需要解析页面的url地址
        :return: selector
        """
        response = self.session.get(url=url, headers=self.headers, verify=True)
        if response.status_code == 200:
            selector = html.fromstring(response.text)
            return selector
        else:
            print("request error, please check! @SKYNE")

    def get_url(self):
        """
        :param
        :return: url_list  返回从首页中banner中的文章的url
        """
        selector = self.parser(self.url)
        url_tmp = list(set(selector.xpath('//h4[@class="media-heading"]/a/@href')))
        """
        :param: url {'/article/220006.html', '/article/219989.html', '/article/220008.html'}
        添加self.url，获取完整的url地址。
        """
        url_list = []
        for url in url_tmp:
            url = "http://www.chanpin100.com" + url
            url_list.append(url)

        return url_list

    def get_news(self, url):
        """
        :param
        url : 需要进行获取信息的url地址
        flag : 标志位，判断是否抓取成功
        news : 字典，存储各信息
        :return: news 正常返回news，错误返回 -1
        """
        news = {}
        flag = None
        try:
            news['url'] = url
            selector = self.parser(url)
            title = selector.xpath('/html/head/title/text()')[0]
            news['author'] = u'产品100'

            tmp = ""
            for i in title:
                if i == '|':
                    break
                tmp += i
            news['title'] = tmp

            content = selector.xpath('//div[@class="article-content-container"]//p')

            article = ""
            temp = []
            cover_list = []
            for i in content:
                url = i.xpath('img/@src')
                temp.append(i.text)
                temp.append(url)
                cover_list.append(url)

            # 去除尾部多余信息
            for i in range (1):
                temp.pop ()

            for i in temp:
                if i:
                    if type(i) == list:
                        article = article + "\n" + "![](" + i[0] + ")" + "\n\n"
                    else:
                        article = article + i.lstrip() + "\n\n"

            summary = ""
            for i in temp:
                if len(summary) > 400:
                    break
                else:
                    if i:
                        if type(i) == list:
                            pass
                        else:
                            summary = summary + i + "\n"

            news['content'] = summary

            news['text'] = article

            for i in cover_list:
                if i:
                    news['cover'] = i[0]
                    break

            news['labels'] = selector.xpath('//ul[@class="tags pull-left"]/li/a/text()')[0]
        except Exception as e:
            print("url=", url, e)
            flag = 1
        if flag == None:
            return news
        else:
            return None


if __name__ == '__main__':
    spider = chanpin()

    url_list = spider.get_url()

    for url in url_list:
        print(spider.get_news(url))