#_*_encoding:utf-8_*_
"""
@Python -V: 3.X
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.12.23
"""

import time

import sqlite3

from sqlite3 import OperationalError

def time_now():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return time_now





def write(news):
    db_name = '../usr/59340ae8f2fe0.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    Title_exist = "SELECT cid FROM typecho_contents WHERE title = " + '\'' +news['title'] +'\''
    flag = cursor.execute(Title_exist).fetchone()
    if cursor and not flag:
        # test = "select * from sqlite_master"  查询表结构

        """cid,title,slug,created,modified,text,[order],authorId,template,type,status,password,commentsNum,allowComment,allowPing,allowFeed,parent,views"""

        # INSERT INTO 插入语句
        Insert_Into_content = "INSERT INTO typecho_contents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        Insert_Into_relationships = "INSERT INTO typecho_relationships VALUES (?, ?)"

        # 选择语句，选出数据库中最后一位的cid
        Seclect = "SELECT cid FROM typecho_contents ORDER BY cid DESC"

        # cid 文章的主键，mid是，文章与所属分类的对应关系记录  1代表科技咨询, 6代表干货知识, 100代表精品书单
        if news['author'] in ['woshipm', 'pmtoo', 'chanpin100', 'zaoduke']:
            mid = 6
        else:
            mid = 1
        # cid是自增主键，因此获取最后一位cid后需要对其加1并转化为字符串类型
        cid = str (int(cursor.execute (Seclect).fetchall ()[0][0]) + 1)

        title = news['title']

        slug = cid

        # 获取那种时间，不是人看的时间
        modified = created = str (int(time.time ()))

        text = "<!--markdown-->" + news['text']

        # 错误的方式，<a href="http://write.blog.csdn.net/postlist" target="_blank">麦田里的码农</a>
        # Values = "(" + cid + ',' + title + ',' + slug + ',' + created + ',' + modified + ',' + text + ',' + """0, 1, NULL, post, publish, NULL, 1, 1, 1, 1, 0, 500 )"""
        values = (cid, title, slug, created, modified, text.encode('utf-8'), 0, 1, '', 'post', 'publish', '', 1, 1, 1, 1, 0, 500)

        # print (Insert_Into_content, Insert_Into_relationships, values)

        cursor.execute (Insert_Into_content, values)

        cursor.execute (Insert_Into_relationships, (cid, mid))
        # 数据库写入后需要提交才会生效，
        conn.commit ()
        # 数据库打开后需要关闭，类似文件操作
        conn.close ()

        print("{}\tDateBase Write Success!@SKYNE\n".format(time_now()))

        return True


    else:

        print ("{}\tDateBase Write Failed, Title Is Exist!@SKYNE\n".format (time_now ()))

        return False


if __name__ == '__main__':
    news = {'url': 'https://www.huxiu.com/article/227432.html', 'link': 'https://m.huxiu.com/article/227432.html', 'title': '京东金融，四年追击 ', 'author': '虎嗅网', 'labels': '金融地产', 'service': 'Article.AddArticle'}
    write(news)