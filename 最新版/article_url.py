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

import sqlite3

def time_now():
    time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return time_now

def remove_repeat(url):
    db_name = "URL.db"

    CREATE_DB = """CREATE TABLE IF NOT EXISTS url (url_id INT(10) PRIMARY KEY, url_string CHAR(100) UNIQUE)"""

    SELECT_URL_ID = """SELECT url_id FROM url ORDER BY url_id DESC"""

    INSERT_URL = """INSERT INTO url( url_id, url_string) VALUES ( %s, %s )"""
    conn = sqlite3.connect(db_name)

    cursor = conn.cursor()

    cursor.execute(CREATE_DB)

    id = cursor.execute(SELECT_URL_ID).fetchone()
    if not id:
        id =1
        # print(INSERT_URL % (id, '\'' +url + '\''))
        cursor.execute(INSERT_URL%(id, '\'' +url + '\''))
    else:
        try:
            cursor.execute(INSERT_URL % (id[0] + 1, '\'' +url + '\''))
            conn.commit()
            conn.close()
            print("{}\tURL Write Success! URL = {} @SKYNE\n".format(time_now(), url))
            return True
        except sqlite3.IntegrityError:
            conn.close()
            print("{}\tURL Write Failed, URL Is Exist! URL = {} @SKYNE\n".format(time_now(), url))
            return False

def isExists(url):
    db_name = "URL.db"

    SELECT_URL_STRING = """SELECT url_id FROM url WHERE url_string = \'""" + url + "\'"

    conn = sqlite3.connect(db_name)

    cursor = conn.cursor()

    if cursor.execute(SELECT_URL_STRING).fetchone():
        print("{}\t URL Is Exist! URL = {} @SKYNE\n".format(time_now(), url))
        return False
    else:
        return True



if __name__ == '__main__':
    url = "sdasdasd"
    # remove_repeat(url)
    isExists('http://www06511')
