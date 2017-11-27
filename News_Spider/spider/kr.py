#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.11.22
"""

from selenium import webdriver

class kr(object):

    def __init__(self):
        self.url = 'https://36kr.com/'

    # 初始化phantomjs，并设置窗口大小，默认300 X 400，返回移动端页面
    def create_phantomJS(self):
        driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 768)
        return driver

    def get_url(self):
        driver = self.create_phantomJS()
        driver.get(self.url)
        # 等待页面加载完成
        driver.implicitly_wait(10)
        url_list = []
        a_tag = driver.find_elements_by_tag_name('a')
        for a in a_tag:
            try:
                # 判断是否是文章链接，是否是banner旋转部分
                judgeFlag = [a.get_attribute('data-stat-click')[0], a.get_attribute('href')[16],
                             a.get_attribute('href')[17]]
                if judgeFlag[0] == 'y' and 'p' in [judgeFlag[1], judgeFlag[2]]:
                    # print(a.get_attribute('href'))
                    url_list.append(a.get_attribute('href'))
            except Exception:
                pass
                # driver.close()
        driver.quit()
        return url_list


    def get_news(self, url):
        driver = self.create_phantomJS()
        driver.get(url)
        # 等待页面加载完成
        driver.implicitly_wait(10)
        news = {}
        flag = None
        try:
            news['link'] = url
            news['author'] = u"36Kr"
            summary = driver.find_element_by_xpath('//div[1]/div/section[@class="summary"]').text
            news['title'] = driver.title + '\n' + summary + '........\n\n点击查看全部'
            news['cover'] = driver.find_element_by_xpath('//section[@class="textblock"]//span/img').get_attribute('src')
            news['labels'] = driver.find_element_by_xpath('//div/span[2]/abbr').text
            news['service'] = 'Article.AddArticle'
            # print(news)
        except Exception as e:
            print("Appear error url=", url)
            flag = 1
        driver.quit()
        if flag == None:
            return news
        else:
            return -1
