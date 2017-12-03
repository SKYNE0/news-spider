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
from selenium.common.exceptions import NoSuchElementException

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
        driver.implicitly_wait(30)
        try:
            news = {}
            news['url'] = url
            news['link'] = url
            news['author'] = u"36Kr"
            summary = driver.find_element_by_xpath('//div[1]/div/section[@class="summary"]').text
            news['title'] = driver.title + '\n' + summary + '........\n\n点击查看全部'
            news['cover'] = driver.find_element_by_xpath('//section[@class="textblock"]//span/img').get_attribute('src')
            news['labels'] = driver.find_element_by_xpath('//div/span[2]/abbr').text
            news['service'] = 'Article.AddArticle'
            driver.quit()
            if not news['cover']:
                news['cover'] = "https://gss3.bdstatic.com/-Po3dSag_xI4khGkpoWK1HF6hhy/baike/crop%3D78%2C0%2C853%2C563%3Bc0%3Dbaike92%2C5%2C5%2C92%2C30/sign=834223da8c18367ab9c6259d1344b3f8/86d6277f9e2f07081b2bc4f3e324b899a901f213.jpg"
                return news
        except NoSuchElementException as e:
            print ("Appear error url=", url, e)
            return None



if __name__ == '__main__':

    url = 'http://36kr.com/p/5105531.html'

    kr = kr()
    url_list = kr.get_url()
    print(url_list)
    for url in url_list:
        print(kr.get_news(url))