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


def sendmail(content):
    from_addr = "1163046964@qq.com"
    password = "jylmcdgl"
    to_addr = '520@skyne.cn'
    server_addr = "smtp.qq.com"
    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = _format_('SKYNE<%s>' % from_addr)
    message['To'] = _format_('Friends<%s>' % to_addr)
    message['Subject'] = Header('SKYNE', 'utf-8').encode()
    # 建立邮件对象，发送信息
    mail_server = smtplib.SMTP(server_addr, 587)
    mail_server.starttls()
    mail_server.set_debuglevel(0)
    mail_server.login(from_addr, password)
    try:
        mail_server.sendmail(from_addr, to_addr, message.as_string())
    except smtplib.SMTPDataError:
        print("Email send error!\n")
    except smtplib.SMTPServerDisconnected:
        print("Faild to connect the mail server!\n")
    mail_server.quit()
    print("Email send success!")

if __name__ == '__main__':
    content = "SKYNE! Something big has happened that the Program is crashed! You must be to fixed the bug! Good luck to you @SKYNE\n"
    sendmail(content)