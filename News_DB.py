#_*_encoding:utf-8_*_
"""
@Python -V: 3.X
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.12.26
"""
import sqlite3

from sqlite3 import IntegrityError

import time

import os

"""
@param
@db_name newsDB.db
@cid 主键，自增
@title_only, title, summary, cover, author, labels, url, link, service, flag 
"""
"""
@:param
@db_name  数据库名称或者路径
@:return 游标对象cursor
"""

seclect_cid = "SELECT cid FROM news ORDER BY cid DESC"

insert_into = "INSERT INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

create_table = "CREATE TABLE news (cid INTEGER PRIMARY KEY, title_only VARCHAR (30) UNIQUE, title MESSAGE_TEXT, summary MESSAGE_TEXT , cover VARCHAR (50), author VARCHAR (10), labels VARCHAR (10), url VARCHAR(30), link VARCHAR(30), service VARCHAR(10) DEFAULT 'Article.AddArticle', flag INTEGER DEFAULT 0)"

seclect_unreade = "SELECT cid, title_only, title, summary, cover, author, labels, url, link, service FROM news WHERE flag = 0"

update_flag = "UPDATE news SET flag = 1 WHERE cid = "


def time_now():
    time_now = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    return time_now


def db_exist(db_name):
    return os.path.exists('news_db.db')

def create_db(db_name):
    if not db_exist(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(create_table)
        conn.commit()
        conn.close()
        print("{}\tName={} Datebase Create Success! @SKYNE".format(time_now(), db_name))
    else:
        print ("{}\tName={} Datebase Is Existed! @SKYNE".format (time_now (), db_name))

"""
@:param
@news 字典类型
@:return True or None
"""
def write_db(news):
    db_name = 'news_db.db'
    # 判断数据库是否存在，怒存在就将创建
    create_db(db_name)

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor ()
    if cursor:
        try:
            cid = str(int(cursor.execute(seclect_cid).fetchall()[0][0]) + 1)
        except IndexError:
            cid = 1
        data = (cid, news['title_only'], news['title'], news['summary'], news['cover'], news['author'], news['labels'], news['url'], news['link'], news['service'], 0)

        try:
            cursor.execute(insert_into, data)
            print("{}\tDate Insert Success! @SKYNE".format(time_now()))
            conn.commit ()
            conn.close ()
            return True
        except IntegrityError as e:
            print("{}\tDate Insert Failed! Error = {} @SKYNE".format(time_now(), e))
            conn.commit ()
            conn.close ()
            return None

    else:
        conn.commit ()
        conn.close ()
        print ("{}\tDate Insert Failed! Error = {} @SKYNE".format(time_now(), 'Cursor Is None'))
        return None

"""
@:param
@:return news or None
"""
def read_db():
    db_name = 'news_db.db'
    try:
        conn = sqlite3.connect(db_name)
    except Exception as e:
        print("Datebase connection failed! Please check! Error = {} @SKYNE".format(e))
        exit()

    cursor = conn.cursor ()
    if cursor:
        # 取出第一个flag=0的记录，也就是没有被读取过的记录
        value = cursor.execute(seclect_unreade).fetchone()
        # 取出后将对应的flag改为1，表示已经读取过
        if value:
            cursor.execute(update_flag + str(value[0]))
            conn.commit ()
            conn.close ()
            # 提交并关闭数据库
            key = ['title_only', 'title', 'summary', 'cover', 'author', 'labels', 'url', 'link', 'service']
            news = {}
            for i in range(len(key)):
                news[key[i]] = value[i + 1]
            print("{}\tDate Read Success! @SKYNE".format(time_now()))
            return news
        else:
            conn.commit ()
            conn.close ()
            print ("{}\tDate Is None So Read Failed! @SKYNE".format (time_now ()))
            return  None
if __name__ == '__main__':
    news = {'url': 'https://www.huxiu.com/article/227432.html', 'link': 'https://m.huxiu.com/article/227432.html', 'title_only': '人待催收行业，还有明？-虎嗅网', 'author': '虎嗅网', 'summary': '在个各行各业都在年终总结、辞旧迎新的日子里，有一个行业可能还顾不上这个，那便是催收业。12月初，现金贷新规出台，平台蜂拥逃离，交给催收机构来清理战场。据一些催收从业者称，近期他们忙得只能接熟人的单子了，大幅涨价也拦不住焦虑的机构，拒接了不少大单子。只是，繁忙的表象之下，大家也迷茫，现金贷的战场打扫干净后，行业的未来在哪里？据媒体报道，近日上海发布现金贷监管细则征求意见稿，明确要求金融', 'title': '不招人待见的催收行业，还有明天吗？-虎嗅网\n在这个各行各业都在年终总结、辞旧迎新的日子里，有一个行业可能还顾不上这个，那便是催收业。12月初，现金贷新规出台，平台蜂拥逃离，交给催收机构来清理战场。据一些催收从业者称，近期他们忙得只能接熟人的单子了，大幅涨价也拦不住焦虑的机构，拒接了不少大单子。只是，繁忙的表象之下，大家也迷茫，现金贷的战场打扫干净后，行业的未来在哪里？据媒体报道，近日上海发布现金贷监管细则征求意见稿，明确要求金融........\n\n点击查看全部', 'cover': 'https://img.huxiucdn.com/article/cover/201712/27/073209097727.jpg?imageView2/1/w/800/h/600/|imageMogr2/strip/interlace/1/quality/85/format/jpg', 'labels': '金融地产', 'service': 'Article.AddArticle'}
    write_db(news= news)
    read_db()