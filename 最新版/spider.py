# _*_encoding:utf-8_*_
"""
@Python -V: 3.X
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.4.14
"""

import requests

from lxml import html

class spiders(object):
    def __init__(self, body):
        self.body = body
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
            # 可能会存在字符编码问题
            selector = html.fromstring(response.text)
            return selector
        else:
            print("request error, please check! @SKYNE")


    """
    :param
    :return: url_list  返回从首页中banner中的文章的url
    """
    def get_url(self):
        selector = self.parser(self.body['domain'])
        url_tmp = list(set(selector.xpath(self.body['getArticleUrl'])))
        """
        :param: url {'/article/220006.html', '/article/219989.html', '/article/220008.html'}
        添加self.url，获取完整的url地址。
        """
        url_list = []
        for url in url_tmp:
            url_list.append(self.body['isFullUrl'] + url)

        return url_list

    """
    :param
    url : 需要进行获取信息的url地址
    flag : 标志位，判断是否抓取成功
    news : 字典，存储各信息
    :return: news 正常返回news，错误返回 -1
    """
    def get_news(self, url):
        news = {}
        flag = None
        try:
            news['url'] = url
            selector = self.parser(url)
            title = selector.xpath(self.body['getTitle'])[0]

            # 去除标题中的网站信息
            tmp = ""
            for i in title:
                if i in ['-', '丨' ,'—', '–', '|']:
                    break
                tmp += i
            news['title'] = tmp

            # 获取文章部分，并重新处理
            content = selector.xpath(self.body['getContent'])
            article = ""
            temp = []
            for i in content:
                # 解决p标签内存在a标签时，获取不到文本的issue
                temp.append(i.xpath('string(.)'))
                if self.body['name'] == 'zaodu':
                    temp.append(i.xpath('a/@href'))
                else:
                    temp.append(i.xpath('img/@src'))

            counter = True
            for i in temp:
                if i:
                    if type(i) == list:
                        # 取第一个图片作为题图
                        if counter:
                            news['cover'] = i[0]
                            counter = False
                        article = article + "\n" + "![](" + i[0] + ")" + "\n\n"
                    else:
                        article = article + i + "\n\n"
            # 组合文章的简介部分
            summary = ""
            for i in temp:
                if len(summary) > 400:
                    break
                else:
                    if i and i != '\n':
                        if type(i) == list:
                            pass
                        else:
                            summary = summary + i.lstrip().replace('\n', '')

            news['content'] = summary.replace('\xa0', '')
            news['text'] = article

            if self.body['name'] == 'huxiu':
                news['cover']=selector.xpath('//div[@class="article-img-box"]/img/@src')[0]
                news['text'] = "![](" + news['cover'] + ")" + "\n" + news['text']

            if self.body['name'] == 'pmtoo':
                news['labels'] = u'产品经理'
            elif self.body['name'] == 'woshipm':
                news['labels']=u'产品项目'
            elif self.body['name'] == 'chanpin':
                news['labels']=u'产品经理'
            else:
                news['labels']=selector.xpath(self.body['getLabels'])[0]

            news['author'] = self.body['getAuthor']
            news['service'] = 'Article.AddArticle'
        except Exception as e:
            print("url=", url, e)
            flag = 1
        if flag == None:
            return news
        else:
            return None


if __name__ == '__main__':

    spider = spiders(['chanpin'])

    url_list = spider.get_url()

    temp = spider.get_news("http://www.chanpin100.com/article/106495")
    print( url_list, temp)
    # for url in url_list:
    #     print(huxiu.get_news(url)['content'])
