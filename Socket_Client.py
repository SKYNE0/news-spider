# _*_ encoding: utf-8 _*_
"""
@Softwave: Pycharm
@Python: 3.X
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.10.22
"""

import socket

import json

import time



def time_now():
    time_now = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    return time_now

"""
@news: 字典类性
"""
def Socket_Send(news):
    HOST = '***********'
    PORT = 3434
    BUFF_SIZE = 8000
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    S.connect((HOST, PORT))
    print("{}\tThe Client Success Connected {} : {}@SKYNE\n".format(time_now(), HOST, PORT))

    try:
        S.send(json.dumps(news).encode('utf-8'))
        data = S.recv(BUFF_SIZE)
        if data:
            print ("{}\tThe Client Is Send Data Success!@SKYNE\n".format (time_now ()))
        else:
            print ("{}\tThe Client Is Send Data Failed! Please Check!@SKYNE\n".format (time_now ()))
    except ConnectionResetError:
        print ("{}\tThe Client Is Send Data Failed! Please Check!@SKYNE\n".format (time_now ()))

    S.close()

if __name__ == '__main__':
    news = {
        'url' : 'https://www.huxiu.com/article/227116.html',
        'title_only' : "中国开征房产税，能绕过产权问题吗？",
        'summary' : '12月20日，财政部部长肖捷在《人民日报》发表题为《加快建立现代财政制度》的署名文章。谈到深化税收制度改革时，肖部长表示将按“立法先行、充分授权、分步推进”的原则推进房地产税立法和实施。他还说到“力争在2019年完成全部立法程序，2020年完成‘落实税收法定原则’的改革任务”。关于房产税的讨论翻来覆去总是“什么时候开征？”“会让房价降下来吗？”其实，首先要想清楚的是为什么征、用到哪里、怎么征。',
        'cover' : 'https://img.huxiucdn.com/article/cover/201712/25/071215300045.jpg?imageView2/1/w/800/h/600/|imageMogr2/strip/interlace/1/quality/85/format/jpg',
    }
    Socket_Send(news)
