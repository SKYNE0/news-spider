# _*_ encoding:utf-8 _*_

"""
@Softwave: Pycharm
@Python: 3.X
@Author: SKYNE
@Contact: 520@skyne.cn 
@Time: 2017.10.27
"""
import requests
from lxml import html
import time

class news_spider():

    def __init__(self):
        self.post_url = "*******************"
        self.huxiu_url = "https://www.huxiu.com"
        self.leiphone_url = "https://www.leiphone.com"
        self.tmtpost_url = "http://www.tmtpost.com"
        self.news_name = ['huxiu', 'leiphone', 'tmtpost']
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",
        }
        self.session = requests.session()
        # self.article_url 用来存储每次获取的文章的url地址，并用来去除重复url地址，判断是否有新的url地址
        self.article_url = []


    # save_info 顾名思义，用来保存获取的信息至本地
    def save_info(self, name, news):
        file_name = name + str(time.strftime("%Y-%m-%d", time.localtime())) + '.txt'

        with open(file_name, 'a+', encoding='utf-8') as f:
            for key, value in news.items():
                f.write(key + ':' +value)
                f.write('\n')
            f.write('=' * 200 + '\n')

    # 使用post的方法，发送抓取信息至指定API接口。
    def post_data(self, news):
        res = self.session.post(url= self.post_url, data= news, headers= self.headers)
        if res.status_code == 200:
            print("Good，发布成功！")

    # 解析url页面
    def parser(self, url):
        response = self.session.get(url= url,headers= self.headers, verify= True)
        if response.status_code == 200:
            selector = html.fromstring(response.text)
            return selector
        else:
            print(u"请求出错，请检查！")

    # 判断每次抓取的url地址是否重复，后来想到新的解决方案。
    # def judge_url_exist(self, url_list):
    #     file_name = 'url_list.txt'
    #     if os.path.exists(file_name):
    #         new_list = []
    #         with open(file_name, 'r+') as f:
    #             for url in f.readlines():
    #                 print(url)
    #                 new_list.append(url)
    #         for url in url_list:
    #             if url in new_list:
    #                 new_list.remove(url)
    #             return new_list
    #     else:
    #         with open(file_name, 'a+') as f:
    #             for url in url_list:
    #                 f.writelines(url)
    #                 f.writelines('\n')
    #             return url_list

    # 获取文章url地址的内容，并筛选有用的信息
    def get_article_url(self, name):
        # article_url 局部变量，存储获取到的文章的url地址
        article_url = []
        if name == 'huxiu':
            selector = self.parser(url=self.huxiu_url)
            url = list(set(selector.xpath('//*[@id="index"]/div[1]/div[1]//a/@href')))
            # print(url)
            # {'/article/220006.html', '/article/219989.html', '/article/220008.html'}
            # 根据长度判断是否为文章的url
            for i in url:
                # 判断是否是文章的url地址，并判断是否已经抓取过，没有抓取过的才会进行添加
                if len(i) == 20 and i not in self.article_url:
                    article_url.append(self.huxiu_url + i)
                self.article_url.append(i)
            # print(article_url)
            return article_url

        elif name == 'leiphone':
            selector = self.parser(url=self.leiphone_url)
            url = list(set(selector.xpath('/html/body/div[2]/div/div[1]/div[1]/div[1]/ul//a/@href')))
            # {'/banner/homepageUrl/id/2560', '/banner/homepageUrl/id/2554', '/banner/homepageUrl/id/2678', '/banner/homepageUrl/id/2665'}
            url = url + list(set(selector.xpath('/html/body/div[2]/div/div[1]/div[1]/div[2]//a/@href')))
            # {'/banner/homepageUrl/id/2574', '/banner/homepageUrl/id/2546', '/banner/homepageUrl/id/2547', '/banner/homepageUrl/id/2540'}
            # print(url)
            for i in url:
                if len(i) == 27 and i not in self.article_url:
                    article_url.append(self.leiphone_url + i)
                self.article_url.append(i)
            # print(article_url)
            return article_url

        elif name == 'tmtpost':
            selector = self.parser(url= self.tmtpost_url)
            url = list(set(selector.xpath('/html/body//section/div[1]/div//div[3]/a/@href')))
            # print(url)
            # {'/2880576.html', '/2883812.html', 'http://www.tmtpost.com/event/t-edge/2017winter/', '/2876844.html'}
            for i in url:
                if len(i) == 13 and i not in self.article_url:
                    article_url.append(self.tmtpost_url + i)
                self.article_url.append(i)
            # print(article_url)
            return article_url

        else:
            print("输入出错，请检查！")



    def get_article_info(self, name):
        article_url = self.get_article_url(name= name)
        # 判断article_url是否为空。不为空则进行抓取内容
        if article_url:
            if name == 'huxiu':
                # news 为字典，用来存储刷选的信息
                news = {}
                for url in article_url:
                    # flag用来判断是否正确抓取了信息，不正确则舍弃
                    flag = None
                    try:
                        news['link'] = url
                        selector = self.parser(url)
                        news['title'] = selector.xpath('/html/head/title/text()')[0]
                        news['author'] = '虎嗅网'
                        # selector.xpath('//div[3]/div[1]/div[2]/a[1]/text()')[0].strip()
                        summary = str(selector.xpath('//div[@class="article-content-wrap"]//p/text()'))[1:200:1].strip("', '")
                        news['title'] = '标题: ' + selector.xpath('/html/head/title/text()')[0] + '\n正文: ' + summary + '........\n\n点击查看全部'
                        news['cover'] = selector.xpath('//div[2]/div[2]/div[4]/img/@src')[0]
                        news['labels'] = selector.xpath('//div[2]/div[2]/div[1]/div/a/text()')[0]
                        news['service'] = 'Article.AddArticle'
                    except IndexError as e:
                        print("url=", url, e)
                        flag = 1
                    if flag == None:
                        print(news)
                        self.save_info(name, news)
                        self.post_data(news)

            elif name == 'leiphone':
                news = {}
                for url in article_url:
                    flag = None
                    try:
                        news['link'] = url
                        selector = self.parser(url)
                        news['author'] = '雷锋网'
                        #selector.xpath('/html/body//section/div/article//a/text()')[0].strip()
                        summary = str(selector.xpath('//div[@class="lph-article-comView"]//p/text()'))[1:200:1]
                        news['title'] = '标题: ' + selector.xpath('/html/head/title/text()')[0] + '\n正文: ' + summary + '........\n\n点击查看全部'
                        news['cover'] = selector.xpath('//img/@src')[2]
                        news['labels'] = selector.xpath('/html/body/div[2]/div/a[2]/text()')[0]
                        news['service'] = 'Article.AddArticle'
                    except IndexError as e:
                        print("url=", url, e)
                        flag = 1
                    if flag == None:
                        print(news)
                        self.save_info(name, news)
                        self.post_data(news)

            elif name == 'tmtpost':
                news = {}
                for url in article_url:
                    flag = None
                    try:
                        news['link'] = url
                        selector = self.parser(url)
                        news['author'] = '钛媒体'
                        #selector.xpath('/html/body/div[5]//div[1]/div[1]/a/span/text()')[0]
                        summary = str(selector.xpath('//div[@class="inner"]//p/text()'))[1:200:1]
                        news['title'] = '标题: ' + selector.xpath('/html/head/title/text()')[0] + '\n正文: ' + summary + '........\n\n点击查看全部'
                        news['cover'] = selector.xpath('//img[@class="aligncenter"]/@src')[0]
                        news['labels'] = selector.xpath('/html/body//section//span[1]/a/text()')[0]
                        news['service'] = 'Article.AddArticle'
                    except IndexError as e:
                        print("url=", url, e)
                        flag = 1

                    if flag == None:
                        print(news)
                        self.save_info(name, news)
                        self.post_data(news)

            else:
                print("出现意外，请检查！")
        else:
            print("没有新的需要抓取的url地址")

    # 用来控制各方法
    def run(self):
        print("程序正在运行，请稍后！")
        name_list = ['huxiu', 'tmtpost', 'leiphone']
        while(True):
            for name in name_list:
                self.get_article_info(name= name)
            # print(self.article_url, type(self.article_url))
            # 每执行一个循环，便会进行一次去除重复的url地址
            self.article_url = list(set(self.article_url))
            # time.localtime() 输出time.struct_time(tm_year=2017, tm_mon=11, tm_mday=1, tm_hour=17, tm_min=41, tm_sec=33, tm_wday=2, tm_yday=305, tm_isdst=0)
            # 晚上九点时，推迟11个小时，至早上8点
            if time.localtime()[3] == 21:
                # 推迟11个小时
                print("推迟11个小时")
                time.sleep(39600)
            else:
                # 推迟三个小时
                print("推迟3个小时")
                time.sleep(10800)
if __name__ == '__main__':

    news_spider = news_spider()

    news_spider.run()