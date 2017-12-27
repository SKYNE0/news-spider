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
import json
import time
class autoSendBlog(object):

    def __init__(self):
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


    def getAccessToken(self):
        app_key = '*********'

        app_secret = '*****************************************'

        redirect_uri = 'https://api.weibo.com/oauth2/default.html'

        authorize = 'https://api.weibo.com/oauth2/authorize?'

        authorize_api = authorize + 'client_id=' + app_key + '&redirect_uri=' + redirect_uri

        print(authorize_api)

        code = input('please enter the code:')

        """
        access_token_api : 'https://api.weibo.com/oauth2/access_token'
        :param
            client_id：申请应用时分配的AppKey。
            client_secret：申请应用时分配的AppSecret。
            grant_type：请求的类型，填写authorization_code
            code：调用authorize获得的code值。
            redirect_uri： 就是创建应用中设置的回调地址
        """

        access_token_api = 'https://api.weibo.com/oauth2/access_token'

        playload = {
            'client_id' : app_key,
            'client_secret' : app_secret,
            'grant_type' : 'authorization_code',
            'code' : code,
            'redirect_uri' : redirect_uri
                    }

        res =self.session.post(url= access_token_api, data= playload, headers= self.headers)

        print(res.text)
        """
        :param
        {
        "access_token":"2.00XCxqJGMxOjrC0cfe0d3b0707AJg2",
        "remind_in":"157679999",
        "expires_in":157679999,
        "uid":"5642404025",
        "isRealName":"true"
        }
        """
        return json.loads(res.text)['access_token']

    def saveImg(self, img_url):

        img_path = 'img/cover.jpg'

        content = self.session.get(url= img_url, headers= self.headers, stream= True)

        with open(img_path, 'wb') as fb:

            for chunk in content.iter_content(chunk_size= 1024):
                fb.write(chunk)




    def SendBlog(self, news):
        # 获取到的access_token 有一定的有效期。
        access_token = '******************657ecfb56XE5fC'

        self.saveImg(img_url= news['cover'])

        if not access_token:
            access_token = self.getAccessToken()
            print(access_token)

        status_update_api = "https://api.weibo.com/2/statuses/share.json"
        # 标题加url不能超过140个字符。刚开始以为url地址不算呢。
        title_len = len(news['title']) + len(news['url']) + 8
        point = 132 - len(news['url'])
        if title_len > 140:
            content = '#' + news['labels'] + '#' + news['title'][0:point:1] + news['url']
        else:
            content = '#' + news['labels'] + '#' + news['title'] + news['url']
        """
            :param
            access_token： 就是我们上一步获得的access_token
            status：要发布的微博文本内容，必须做URLencode，内容不超过140个汉字
            """
        playload = {
                'access_token' : access_token,
                'status' : content,
                        }

        files = {
            "pic" : open('img/cover.jpg', 'rb')
                 }

        res = self.session.post(url= status_update_api, data= playload, files= files, headers= self.headers)

        res_dict = json.loads(res.text)
        if 'error' in res_dict.keys():
            if res_dict['error_code'] == 20005:
                self.session.post (url=status_update_api, data=playload, headers=self.headers)
                return 1
            else:
                print('Blog seng error! please check the error = {}! @SKYNE'.format(res_dict['error']))
                return str(res_dict['error_code']) + res_dict['error']
        else:
            # print('Good, Blog is send success! @SKYNE')
            return 1

if __name__ == '__main__':
#     news = {
#         'url' : 'https://www.huxiu.com',
#         'title' : '近日，并赔偿网易经济损失2000万元。网易CEO丁磊回应表示，网易对游戏主播与直播平台持开放,磊回应表示，网易对游戏主播与直播平台'
# ,
#         'cover' : 'https://img.huxiucdn.com/article/cover/201711/29/065740692326.jpg?imageView2/1/w/800/h/600/|imageMogr2/strip/interlace/1/quality/85/format/jpg',
#         'labels' : 'test'
#     }
     Blog = autoSendBlog()

     Blog.getAccessToken()
