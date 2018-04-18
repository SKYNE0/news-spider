#_*_encoding:utf-8_*_
"""
@Python -V: 3.X 
@SoftWave: Pycharm
@OS: Win10
@Author: SKYNE
@Contact: 520@skyne.cn
@Time: 2017.11.22
"""
import fileinput
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr


# 定义一个用于格式化邮件地址的函数
def _format_(addr):
    name, addr = parseaddr(addr)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sendmail(content,addr):
    from_addr = "520@skyne.cn"
    password = "******************"
    server_addr = "smtp.qq.com"
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = _format_('爬虫任务<%s>' % from_addr)
    message['To'] = _format_('Friends<%s>' % addr)
    message['Subject'] = Header('所有网址已爬取完毕，程序自动退出', 'utf-8').encode()
    # 建立邮件对象，发送信息
    mail_server = smtplib.SMTP_SSL(server_addr, 465)
    # mail_server.starttls()
    # mail_server.set_debuglevel(0)
    mail_server.login(from_addr, password)
    try:
        mail_server.sendmail(from_addr, addr, message.as_string())
        print ("Email send success! {}\n".format(addr))

    except Exception as e:
        print("Email send error = {}! {}\n".format(addr, e))

    mail_server.quit()


if __name__ == '__main__':
    content = """asdbhqajdl;kjsdl;kqwdja;lksjd;alskdjasd"""
    addr = "520@skyne.cn"
    sendmail(content,addr)