from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from my_package import crawler


class PEmail(object):
    def __init__(self, from_addr, to_addr, cc_addr, smtp_server, password):  # 初始化类
        try:
            self.from_addr = from_addr  # 发件人账号
            self.to_addr = to_addr  # 收件人地址
            self.cc_addr = cc_addr  # 抄送人地址
            self.smtp_server = smtp_server  # smtp服务器地址
            self.password = password  # 发送密码
            #self.msg = ''
        except Exception as err:
            crawler.log('邮件发送类初始化异常', 0)
            crawler.log(err, 0)

    def init_mail_content(self, mail_content, mail_title):
        try:
            self.msg = MIMEText(mail_content, 'plain', 'utf-8')
            self.msg['From'] = formataddr(["招标自动抓取系统", self.from_addr])
            # self.msg['To'] = formataddr([self.to_addr, self.to_addr])
            self.msg['To'] = self.to_addr
            self.msg['Cc'] = self.cc_addr
            self.msg['Subject'] = Header(mail_title, 'utf-8').encode()
            self.msg['Date'] = time.strftime("%Y-%m-%d %H:%M:%S") + ' +0800'  # 设置时间，后面的是时区
        except Exception as err:
            crawler.log('邮件内容初始化异常', 0)
            crawler.log(err, 0)

    def init_mail_content_with_file(self, mail_content, mail_title):
        try:
            self.msg = MIMEMultipart()
            self.msg['Subject'] = Header(mail_title, 'utf-8').encode()
            self.msg['From'] = formataddr(["招标自动抓取系统", self.from_addr])
            # self.msg['To'] = formataddr([self.to_addr, self.to_addr])
            self.msg['To'] = self.to_addr
            self.msg['Cc'] = self.cc_addr
            self.msg['Date'] = time.strftime("%Y-%m-%d %H:%M:%S") + ' +0800'  # 设置时间，后面的是时区
        # 下面是文字部分，也就是纯文本
            puretext = MIMEText('三运营商抓取信息，')
            self.msg.attach(puretext)



        # xlsx类型的附件
            xls_name1 = '联通' + str(time.strftime("%y%m%d")) + '.xls'
            xls_name2 = '电信' + str(time.strftime("%y%m%d")) + '.xls'
            xls_name3 = '移动' + str(time.strftime("%y%m%d")) + '.xls'


            xlsxpart = MIMEApplication(open(xls_name1, 'rb').read())
            xlsxpart.add_header('Content-Disposition', 'attachment', filename=xls_name1)
            self.msg.attach(xlsxpart)

            xlsxpart = MIMEApplication(open(xls_name2, 'rb').read())
            xlsxpart.add_header('Content-Disposition', 'attachment', filename=xls_name2)
            self.msg.attach(xlsxpart)

            xlsxpart = MIMEApplication(open(xls_name3, 'rb').read())
            xlsxpart.add_header('Content-Disposition', 'attachment', filename=xls_name3)
            self.msg.attach(xlsxpart)

        except Exception as err:
            crawler.log('邮件内容初始化异常', 0)
            crawler.log(err, 0)

    def send_mail(self, mail_content, mail_title):
        try:
            self.init_mail_content(mail_content, mail_title)
            server = smtplib.SMTP_SSL(self.smtp_server, 465)
            #server.set_debuglevel(1) #邮件发送调试开关
            server.login(self.from_addr, self.password)
            # server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
            server.sendmail(self.from_addr, self.to_addr.split(',')+self.cc_addr.split(','), self.msg.as_string())
            server.quit()
        except Exception as err:
            crawler.log('邮件发送动作异常', 0)
            crawler.log(err, 0)

    def send_mail_with_file(self, mail_content, mail_title):
        try:
            self.init_mail_content_with_file(mail_content, mail_title)
            #client = smtplib.SMTP()
            #client.connect('smtp.163.com')
            server = smtplib.SMTP_SSL(self.smtp_server, 465)
            #client.login(username, password)
            server.login(self.from_addr, self.password)
            #client.sendmail(sender, receivers, msg.as_string())
            # server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
            server.sendmail(self.from_addr, self.to_addr.split(',')+self.cc_addr.split(','), self.msg.as_string())
            #client.quit()
            server.quit()
            crawler.log('附件邮件已发送', 0)
        except Exception as err:
            crawler.log('带附件邮件发送动作异常', 0)
            crawler.log(err, 0)

