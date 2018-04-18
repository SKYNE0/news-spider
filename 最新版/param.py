# _*_encoding:utf-8_*_
"""
@Python -V: 3.X
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2018.4.14
"""

param = {
    'huxiu' : {
        'name' : 'huxiu',
        'domain' : 'https://www.huxiu.com',
        'isFullUrl' : 'https://www.huxiu.com',
        'getArticleUrl' : '//*[@id="index"]//div[@class="big-pic-box"]//a/@href',
        'getTitle' : '/html/head/title/text()',
        'getAuthor' : u'虎嗅网',
        'getContent' : '//div[@class="article-content-wrap"]//p',
        'getLabels' : '//div[@class="column-link-box"]/a/text()',
        },
    'tmtpost': {
        'name': 'tmtpost',
        'domain': 'http://www.tmtpost.com',
        'isFullUrl' : 'http://www.tmtpost.com',
        'getArticleUrl': '/html/body//section/div[1]/div//div[3]/a/@href',
        'getTitle': '/html/head/title/text()',
        'getAuthor': u'钛媒体',
        'getContent': '//div[@class="inner"]//p',
        'getLabels': '/html/body//section//span[1]/a/text()',
        },
    'zaodu': {
        'name': 'zaodu',
        'domain': 'https://www.zaodula.com',
        'isFullUrl' : '',
        'getArticleUrl': '//header/h2[@class="entry-title"]/a/@href',
        'getTitle': '/html/head/title/text()',
        'getAuthor': u'早读课',
        'getContent': '//div[@class="single-content"]//p',
        'getLabels': '//div[@class="single-cat"]/a/text()',
        },
    'woshipm': {
        'name': 'woshipm',
        'domain': 'http://www.woshipm.com/category/pmd',
        'isFullUrl': '',
        'getArticleUrl': '//h2[@class="post-title"]/a/@href',
        'getTitle': '/html/head/title/text()',
        'getAuthor': u'人人都是产品经理',
        'getContent': '//div[@class="grap"]//p',
        'getLabels': u"产品项目",
    },
    'chanpin': {
        'name': 'chanpin',
        'domain': 'http://www.chanpin100.com/pm',
        'isFullUrl': 'http://www.chanpin100.com',
        'getArticleUrl': '//h4[@class="media-heading"]/a/@href',
        'getTitle': '/html/head/title/text()',
        'getAuthor': u'产品100',
        'getContent': '//div[@class="article-content-container"]//p',
        'getLabels': u"产品经理",
        },
    'pmtoo': {
        'name': 'pmtoo',
        'domain': 'http://www.pmtoo.com/article/category/产品经理',
        'isFullUrl': '',
        'getArticleUrl': '//h2[@class="title"]/a/@href',
        'getTitle': '/html/head/title/text()',
        'getAuthor': u'产品中国',
        'getContent': '//div[@class="post-con mobantu"]//p',
        'getLabels': u"产品经理",
        }

    }