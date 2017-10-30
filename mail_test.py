import time
import socket
import platform, urllib.request
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# from_addr = input('From: ')
# password = input('Password: ')
# to_addr = input('To: ')
# smtp_server = input('SMTP server: ')
from_addr = 'get_data_server@hollycrm.com'
password = '12345678Az'
to_addr = 'yuxiao1@hollycrm.com'
cc_addr = ''
smtp_server = 'smtp.hollycrm.com'

msg = MIMEText('看看能否显示收件人、抄送人，是否是多个联系人', 'plain', 'utf-8')
msg['From'] = _format_addr(from_addr)
# msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['To'] = to_addr
msg['Cc'] = cc_addr
msg['Subject'] = Header('测试多方发送、抄送', 'utf-8').encode()
msg['Date'] = time.strftime("%Y-%m-%d %H:%M:%S") + ' +0800'  # 设置时间，后面的是时区
'''
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, to_addr.split(',')+cc_addr.split(','), msg.as_string())
server.quit()
'''
if __name__ == "__main__":
    '''
    if platform.platform().find('Windows') >= 0:
        print('Win')
    elif platform.platform().find('Linux') >= 0:
        print('Linux')
    else:
        print('Other')

'''
    timeout = 10
    socket.setdefaulttimeout(timeout)
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    url_ = 'http://www.google.com/'
    try:
        original_data = urllib.request.urlopen(url_).read()
        original_data = original_data.decode('gbk')
        print(original_data)
    except Exception as err:
        print(err)
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

