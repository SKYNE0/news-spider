#_*_encoding:utf-8_*_
"""
@Python -V: 3.X
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.4.15
"""

import time

import pymysql

def time_now():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return time_now


def write(news):
    # wp_posts
    # ID：自增唯一ID
    # post_author：对应作者ID
    # post_date：发布时间
    # post_date_gmt：发布时间（GMT + 0
    # 时间）
    # post_content：正文
    # post_title：标题
    # post_excerpt：摘录
    # post_status：文章状态（publish / auto - draft / inherit等）
    # comment_status：评论状态（open / closed）
    # ping_status：PING状态（open / closed）
    # post_password：文章密码
    # post_name：文章缩略名
    # to_ping：未知
    # pinged：已经PING过的链接
    # post_modified：修改时间
    # post_modified_gmt：修改时间（GMT + 0
    # 时间）
    # post_content_filtered：未知
    # post_parent：父文章，主要用于PAGE
    # guid：未知
    # menu_order：排序ID
    # post_type：文章类型（post / page等）
    # post_mime_type：MIME类型
    # comment_count：评论总数
    # 查询相关数据表的主键末值
    SELECT_LAST_ID = """SELECT ID FROM  wp_posts ORDER BY ID DESC"""
    SELECT_POSTMETA_ID="""SELECT meta_id FROM  wp_postmeta ORDER BY meta_id DESC"""
    SELECT_TERM_ID = """SELECT term_id FROM  wp_terms ORDER BY term_id DESC"""
    SELECT_TERM_TAXONOMY_ID = """SELECT term_taxonomy_id FROM  wp_term_taxonomy ORDER BY term_taxonomy_id DESC"""
    SELECT_TERM_REATIONSHIPS_ID = """SELECT object_id FROM  wp_term_relationships ORDER BY object_id DESC"""

    # 插入数据表的相关语句
    INSERT_POST_SQL = """INSERT INTO wp_posts(ID, post_author, post_date, post_date_gmt,post_content,post_title, post_excerpt, post_status, comment_status, ping_status, post_password,post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered,post_parent, guid, menu_order, post_type,post_mime_type,comment_count) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    INSERT_TERM = """INSERT INTO wp_terms (term_id, name, slug, term_group) VALUES (%s, %s, %s, %s)"""
    INSERT_POSTMETA="""INSERT INTO wp_postmeta (meta_id, post_id, meta_key, meta_value) VALUES (%s, %s, %s, %s)"""
    INSERT_TERM_TAXONOMY = """INSERT INTO wp_term_taxonomy (term_taxonomy_id,term_id, taxonomy, description, parent, count) VALUES (%s, %s, %s, %s, %s, %s)"""
    INSERT_TERM_REATIONSHIPS = """INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order) VALUES (%s, %s, %s)"""

    # 连接MySQL服务器
    conn = pymysql.connect(host = '***********', port = 3306, user ='****', passwd = '***********', db ='wordpress', charset = 'utf8')
    cursor = conn.cursor()
    cursor.execute(SELECT_LAST_ID)

    # 下面获取所需的INSERT的元素内容
    last_id = cursor.fetchone()[0] + 1
    time = '\'' + str(time_now()) + '\''
    guid = '\'' +  "http://jingyu.in/?p=" + str(last_id) + '\''
    content = '\'' +  news['text'] + '\''
    title =  '\'' +  news['title'] + '\''
    excerpt = '\'' +  news['content'][0:200:1] + '.....\''
    values = (last_id, 1, time, time, content, title, excerpt , '\'pending\'', '\'open\'', '\'open\'', '\'\'', last_id, '\'\'', '\'\'', time, time, '\'\'', 0, guid, 0, '\'post\'', '\'\'', 0)
    # print(INSERT_POST_SQL%(values))
    cursor.execute(INSERT_POST_SQL%(values))

    #  文章的主键，term_id是，文章与所属分类的对应关系记录  2代表科技咨询, 3代表干货知识, 100代表精品书单
    if news['author'] in [u'人人都是产品经理', u'产品中国', u'产品100', u'早读课']:
        term_id = 3
    elif news['author'] == u'word' :
        term_id = 606
    elif news['author'] == u'ppt':
        term_id= 607
    elif news['author'] == u'excel' :
        term_id = 602
    else:
        term_id = 2

    # 将标签插入term表中
    tag = '\'' +  news['labels'] + '\''
    cursor.execute(SELECT_TERM_ID)
    last_term_id = cursor.fetchone()[0] + 1
    # print(INSERT_TERM%(last_term_id, tag, last_term_id, 0))
    cursor.execute(INSERT_TERM%(last_term_id, tag, last_term_id, 0))

    # 建立标签的分类方法，即存储是分类还是标签
    cursor.execute(SELECT_TERM_TAXONOMY_ID)
    last_taxonomy_id = cursor.fetchone()[0] + 1
    cursor.execute(INSERT_TERM_TAXONOMY%(last_taxonomy_id, last_term_id, '\'post_tag\'', '\'\'', 0, 0))
    # cursor.execute(INSERT_TERM_TAXONOMY%(last_taxonomy_id + 1, term_id, '\'category\'', '\'\'', 0, 0))

    cursor.execute(SELECT_POSTMETA_ID)
    post_meta_id= cursor.fetchone()[0] + 1
    # 文章的元类字段，就是标识文章的一些信息
    cursor.execute(INSERT_POSTMETA%(post_meta_id, last_id, '\'_wpcom_metas\'', '\'a:1:{s:14:"copyright_type";s:1:"0";}\''))
    cursor.execute(INSERT_POSTMETA % (post_meta_id + 1, last_id, '\'_wpcom_is_markdown\'', 1))
    # 建立文章与分类，标签之间的关系
    cursor.executemany(INSERT_TERM_REATIONSHIPS,[(last_id, last_taxonomy_id, 0 ), (last_id, term_id, 0 )])

    # 尝试提交数据库，失败则回滚操作
    try:
        conn.commit()
        conn.close()
        print(time, '\tThe news write MySql Success @SKYNE\n')
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        print(time, '\tThe news write MySql Failed @SKYNE\n')
        return False




if __name__ == '__main__':
    news = {'url': 'https://www.hxiu.comarticle/227432.html', 'link': 'https//mhuxiu.com/article/22743.html', 'title': 'vfkhvbjhbjkhbhjmkjh', 'text' : 'a' * 250, 'content' : 'a' * 250, 'author': 'word', 'labels': '金融地产', 'service': 'Article.AddArticle'}
    write(news)
