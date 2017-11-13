# _*_ encoding:utf-8 _*_

"""
@Softwave: Pycharm
@Python: 3.X
@Author: SKYNE
@Contact: 520@skyne.cn 
@Time: 2017.11.12
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import requests

class kr_spider():
    # 说来奇怪，不知道为什么在其他方法中执行selenium打开phantomjs的操作会导致无法提取主页文章的url地址，而放在构造方法就可以。
    def __init__(self):
        self.post_url = "http://123.206.254.253/Cetus/Public/cetus/"
        self.url = "https://36kr.com/"
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
        # 默认窗口大小为300 X 400，会返回一个移动端页面
        self.driver = webdriver.PhantomJS()
        # print(driver.get_window_size())
        self.driver.set_window_size(1024, 768)
        # 以下代码放在方法中不能得到结果，没搞明白具体什么导致的。暂时放在构造方法中
        self.driver.get(self.url)
        self.handle = self.driver.current_window_handle
        # 等待页面加载完成
        self.driver.implicitly_wait(10)
        # print(driver.page_source)
        # driver.save_screenshot('test1.png')
        # 获取主页中所有的a标签
        a_tag = self.driver.find_elements_by_tag_name('a')
        self.article_url = []
        for a in a_tag:
            try:
                # 判断是否是文章链接，是否是banner旋转部分
                judgeFlag = [a.get_attribute('data-stat-click')[0],
                             a.get_attribute('href')[16],
                             a.get_attribute('href')[17]]
                if judgeFlag[0] == 'y' and 'p' in [judgeFlag[1], judgeFlag[2]]:
                    # print(a.get_attribute('href'))
                    self.article_url.append(a.get_attribute('href'))
                    # print(a.get_attribute('href'))
                    # print(a.get_attribute('data-stat-click'))
                    # print(text.get_attribute('href')[17], text.get_attribute('href')[16])
            except Exception :
                pass
            # driver.close()

    def time_now(self):
        time_now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return time_now

    def post_data(self, news):
        res = self.session.post(url= self.post_url, data= news, headers= self.headers)
        if res.status_code == 200:
            print(self.time_now(), u"\tGood, Send success")

    # 传入需要获取信息的url列表article_url
    def get_article_info(self, article_url):
        for url in article_url:
            flag = None
            news = {}
            self.driver.get(url)
            time.sleep(5)
            try:
                news['link'] = url
                news['author'] = u"36Kr"
                summary = self.driver.find_element_by_xpath('//div[1]/div/section[@class="summary"]').text
                news['title'] = self.driver.title + '\n' + summary + '........\n\n点击查看全部'
                news['cover'] = self.driver.find_element_by_xpath('//section[@class="textblock"]//span/img').get_attribute('src')
                news['labels'] = self.driver.find_element_by_xpath('//div/span[2]/abbr').text
                news['service'] = 'Article.AddArticle'
                # print(news)
            except NoSuchElementException as e:
                print(self.time_now(), "\tAppear error url=", url)
                flag = 1
            if flag == None:
                print(self.time_now(), "\t36kr success {}".format(url))
                self.post_data(news)

    def quit_self(self):
        # 窗口不能正确关闭，会导致，新开的窗口不断增加，内存暴涨。
        self.driver.quit()
        # 此处不能用close方法，close关闭窗口，不退出程序，继续后台运行，quit方法退出程序。不保留后台程序。
        print(u'Phantomjs is quit!')
        #小插曲，没处理好phantomjs的正确退出，测试时上个厕所回来，CPU暴涨至94，鼠标卡的都不见了，0.0

def ctrl_spider():
    print(u"\tProgram runing please waiting")
    counter = 0
    article_url = []
    while(True):
        counter += 1
        spider = kr_spider()
        print(spider.time_now(), "\t{}th queries are in progress".format(counter))
        # 判断文章的url地址是否已经抓取过，抓取过不再抓取。
        if article_url:
            article_url_new = []
            for url in spider.article_url:
                if url not in article_url:
                    article_url_new.append(url)
            if article_url_new:
                spider.get_article_info(article_url_new)
            else:
                print(spider.time_now(), u"\tno new url need spider")
        else:
            article_url = list(set(article_url + spider.article_url))
            spider.get_article_info(article_url)

        # 最后无论是否抓取信息，都要退出phantomjs，
        spider.quit_self()

        if time.localtime()[3] > 21:
        # 推迟11个小时
            print(spider.time_now(), u"\tProgram delay 11 h")
            time.sleep(25200)
            # 清除存储的文章的url地址,
            article_url = []
        else:
            # 推迟一个小时
            print(spider.time_now(), u"\tProgram delay 1 h")
            time.sleep(3600)


if __name__ == '__main__':
    ctrl_spider()