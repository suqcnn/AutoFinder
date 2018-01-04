﻿import os
import re
import time
import socket
import platform
import urllib.request
import requests
import requests.packages.urllib3.util.ssl_
from my_package.pemail import PEmail
from my_package import crawler
from selenium import webdriver
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
socket.setdefaulttimeout(8)
admin_mail = PEmail('get_data_server@hollycrm.com',                   # 发件地址
                    'lill@hollycrm.com',                              # 收件地址（多个用逗号分隔）
                    'zhaojd@hollycrm.com,maqiang@hollycrm.com,masn@hollycrm.com,wanghs@hollycrm.com,Zhangbo2@hollycrm.com,liying1@hollycrm.com,huanggy@hollycrm.com,lizhe@hollycrm.com,liyl@hollycrm.com,yuxiao1@hollycrm.com',    # 抄送地址（多个用逗号分隔）
                    'smtp.hollycrm.com',                              # 发件服务器
                    '12345678Az')                                     # 发件邮箱密码
mails = [admin_mail]

province_keywords = ['北京', '山西', '河北', '湖北', '辽宁', '新疆', '江西', '内蒙', '浙江', '广州', '海南', '安徽']
all_province_keywords = ['北京', '广东', '山东', '江苏', '河南', '上海', '河北', '浙江', '香港', '陕西', '湖南', '重庆', '福建', '天津', '云南', '四川',
                          '广西', '安徽', '海南', '江西', '湖北', '山西', '辽宁', '台湾', '黑龙江', '内蒙古', '澳门', '贵州', '甘肃', '青海', '新疆',
                         '西藏', '吉林', '宁夏']
business_keywords = ['AI', 'IVR', 'NPS', '拨测', '存量', '电渠', '电子渠道', '短信', '多媒体', '分析', '服务预判', '工单', '公众号', '固网', '呼叫', '互联网', '回访', '稽核', '集成', '监控', '接续', '精准服务', '客服', '宽带', '门户', '模型', '全媒体', '人工', '数据', '调查', '投诉', '挖掘', '外包', '外呼', '微信', '维系', '协助运营', '一体化', '营销', '用户行为', '舆情', '运营', '知识库', '质检', '智慧', '智能', '自媒体']
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

def sleeptime(hour, min, sec):  # 休眠时间设置
    return hour * 3600 + min * 60 + sec

def send_all(mail_content, mail_title):
    for value in mails:
        try:
            value.send_mail(mail_content, mail_title)
            crawler.log('发送邮件给 ' + value.to_addr + ':' + mail_content[:int(len(mail_content)/4)] + '...')
        except Exception as err:
            crawler.log('发送给'+ value.to_addr + '的邮件发送出现问题')
            crawler.log(err, 0)
            # time.sleep(tmp)

# 中国电信招标项目列表
telecom_project_list = {}
# 中国联通招标项目列表
chinaunicom_project_list = {}
# 中国移动招标项目列表
chinamobile_project_list = {}
# 中国铁塔招标项目列表
chinatower_project_list = {}

def seach_telecom_project():
    # 中国电信阳光采购网网址
    #url = "http://caigou.chinatelecom.com.cn:8001/ESCM/biddoc/getListProvince.do?paging.pageSize=40"
    url = "https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?paging.pageSize=40"
    # res = requests.get("https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT",
    #                    verify=False)
    # 读取原始网页数据
    try:
        #original_data = urllib.request.urlopen(url, verify=False).read()
        #original_data = original_data.decode('GBK')
        res = requests.get(url, verify=False)
        original_data = res.text
        #print(original_data)
    except Exception as err:
        crawler.log(err, 0)

    # <a></a>之间整个链接的提取规则
    link_rule = r'<a (.*?)/a>'

    # <a></a>之间URL的提取规则
    url_rule = r"'(.*?)','(.*?)'"

    # <a></a>之间title的提取规则
    title_rule = '">(.*?)<'

    # 获取原始整个链接
    original_links = re.findall(link_rule, original_data, re.S | re.M)
    try:
        for value in original_links:
            url = re.findall(url_rule, value, re.S | re.M)  # 获取url
            title = re.findall(title_rule, value, re.S | re.M)  # 获取招标项目名称
            if len(title) and len(url):
                if not (title[0] in telecom_project_list):
                    url = list(url[0])
                    telecom_project_list[title[0]] = url[0]
                    temp_text = "https://caigou.chinatelecom.com.cn/MSS-PORTAL/account/viewad.do?category=" + url[1] + "&id=" + url[0]
                    #temp_text1 = "https://caigou.chinatelecom.com.cn/MSS-PORTAL/purchaseannouncebasic/viewHome.do?id="
                    #temp_text = temp_text + telecom_project_list[title[0]]
                    #temp_text1 = temp_text1 + telecom_project_list[title[0]]
                    txt = r'招标信息：' + title[0] + ' ,\n链接：' + temp_text
                    #print(txt)
                    logtxt = r'招标信息：' + title[0]
                    crawler.log(logtxt, 0)
                    this_province = crawler.finderX(all_province_keywords, txt)
                    this_genre = crawler.finderX(business_keywords, txt)
                    crawler.save_xls('电信'+str(time.strftime("%y%m%d")), 0, province=this_province, genre=this_genre,
                                     business=title[0], url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                    if crawler.finderX(province_keywords, txt):  # 判断是否是重点省分项目
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('电信'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business=title[0],
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点省分重点项目 请注意')  # 判断是否是重点类型项目
                    else:
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('电信'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business=title[0],
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点项目 请注意')  # 判断是否是重点类型项目
    except Exception as err:
        crawler.log(err, 0)
    crawler.log("完成抓取，目前【电信】共抓取：" + str(len(telecom_project_list)) + "条记录")

def seach_chinaunicom_project():
    # 中国联通采购网网址
    url = "http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?"

    # 读取原始网页数据
    try:
        original_data = urllib.request.urlopen(url).read()
        original_data = original_data.decode('GBK')
    except Exception as err:
        crawler.log(err, 0)

    # <span></span>之间整个链接的提取规则
    link_rule = r'<span (.*?)</span>'

    # 原始链接段之间URL的提取规则
    url_rule = r'window.open(.*?)","","height=600,width=900.*?'

    # 原始链接段之间之间title的提取规则
    title_rule = r"title='(.*?)'>.*?"

    # 获取原始整个链接
    original_links = re.findall(link_rule, original_data, re.S | re.M)
    try:
        for value in original_links:
            url = re.findall(url_rule, value, re.S | re.M)  # 获取url
            title = re.findall(title_rule, value, re.S | re.M)  # 获取招标项目名称
            if len(title) and len(url):
                if not (title[0] in chinaunicom_project_list):
                    chinaunicom_project_list[title[0]] = url[0]
                    temp_text = "http://www.chinaunicombidding.cn/"
                    temp_text = temp_text + str(chinaunicom_project_list[title[0]])[3:]
                    txt = r'招标信息：' + title[0] + ' ,\n链接：' + temp_text
                    logtxt = r'招标信息：' + title[0]
                    crawler.log(logtxt, 0)
                    this_province = crawler.finderX(all_province_keywords, txt)
                    this_genre = crawler.finderX(business_keywords, txt)
                    crawler.save_xls('联通'+str(time.strftime("%y%m%d")), 0, province=this_province, genre=this_genre,
                                     business=title[0], url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                    if crawler.finderX(province_keywords, txt):  # 判断是否是重点省分项目
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('联通'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business=title[0],
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点省分重点项目 请注意')  # 判断是否是重点类型项目
                    else:
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('联通'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business=title[0],
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点项目 请注意')  # 判断是否是重点类型项目
    except Exception as err:
        crawler.log(err, 0)
    crawler.log("完成抓取，目前【联通】共抓取：" + str(len(chinaunicom_project_list)) + "条记录")

def seach_chinamobile_project():
    # 中移动采购网网址
    url = "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"
    # 读取原始网页数据
    try:
        if platform.platform().find('Linux') >= 0:
            drive = webdriver.PhantomJS(executable_path=r"phantomjs")
        elif platform.platform().find('Windows') >= 0:
            drive = webdriver.PhantomJS(executable_path=r"phantomjs-2.1.1-windows/bin/phantomjs.exe")
        else:
            drive = webdriver.PhantomJS()
        drive.get(url)
        time.sleep(5)
        html = drive.page_source.encode('utf-8')
        #print(html.decode('utf-8'))
        drive.quit()
        original_data = html.decode('utf-8')
    except Exception as err:
        crawler.log(err, 0)

    # <a></a>之间整个链接的提取规则
    link_rule = r'<tr class=(.*?)</tr>'

    # <a></a>之间URL的提取规则
    url_rule = r'selectResult(.*?)">'

    # <a></a>之间title的提取规则
    title_rule = r'"#this"(.*?)</a>'

    # 获取原始整个链接
    original_links = re.findall(link_rule, original_data, re.S | re.M)
    try:
        for value in original_links:
            url = re.findall(url_rule, value, re.S | re.M)  # 获取url
            title = re.findall(title_rule, value, re.S | re.M)  # 获取招标项目名称
            if len(title) and len(url):
                if not (title[0] in chinamobile_project_list):
                    chinamobile_project_list[title[0]] = url[0]
                    temp_text = "https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="
                    temp_text = temp_text + chinamobile_project_list[title[0]][2:-2]
                    title_text = title[0]
                    str1 = 'title='
                    if title_text.find(str1) > 0:
                        title_text = title_text[title_text.find(str1)+7:title_text.find('">')]
                    else:
                        title_text = title_text[1:]
                    txt = r'招标信息：' + title_text + ' ,\n链接：' + temp_text
                    logtxt = r'招标信息：' + title[0]
                    crawler.log(logtxt, 0)
                    this_province = crawler.finderX(all_province_keywords, txt)
                    this_genre = crawler.finderX(business_keywords, txt)
                    crawler.save_xls('移动'+str(time.strftime("%y%m%d")), 0, province=this_province, genre=this_genre,
                                     business= title_text, url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                    if crawler.finderX(province_keywords, txt):  # 判断是否是重点省分项目
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('移动'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business= title_text,
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点省分重点项目 请注意')  # 判断是否是重点类型项目
                    else:
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('移动'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business= title_text,
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点项目 请注意')  # 判断是否是重点类型项目
    except Exception as err:
        crawler.log(err, 0)
    crawler.log("完成抓取，目前【移动】共抓取：" + str(len(chinamobile_project_list)) + "条记录")


def get_tower(_url, _headers, _payload):
    response = requests.post(_url, headers=_headers, data=_payload,).json()['obpNotice']
    return response


def seach_chinatower_project():
    # 中国铁塔采购网网址
    tower_url = 'http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.main.index.obphomepage.queryNoticeDetails.biz.ext'
    tower_headers = {
        'Host': 'www.tower.com.cn',
        'Connection': 'keep-alive',
        'Content-Length': '229',
        'Origin': 'http://www.tower.com.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_purchaseNoticeType=2&_resultsNoticeType=2',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    tower_payload = '{"noticeTitle":"","effectTime":"","failureTime":"","noticeType":"null","purchaseNoticeType":"2","resultsNoticeType":"2","level":"","pageIndex":0,"pageSize":50,"sortField":"failure_time","sortOrder":"desc","page":{"begin":0,"length":50}}'

    # 读取原始网页数据
    try:
        original_links = get_tower(tower_url, tower_headers, tower_payload)
    except Exception as err:
        crawler.log(err, 0)

    try:
        for value in original_links:
            # 代码统一，把url和title都转成list，下面的代码就不用改了
            url = [value['id']]
            title = [value['notice_title']]
            if len(title) and len(url):
                if not (title[0] in chinatower_project_list):
                    chinatower_project_list[title[0]] = url[0]
                    temp_text = "http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_notice=6&_id="
                    temp_text = temp_text + str(chinatower_project_list[title[0]])
                    txt = r'招标信息：' + title[0] + ' ,\n链接：' + temp_text
                    logtxt = r'招标信息：' + title[0]
                    crawler.log(logtxt, 0)
                    this_province = crawler.finderX(all_province_keywords, txt)
                    this_genre = crawler.finderX(business_keywords, txt)
                    crawler.save_xls('铁塔'+str(time.strftime("%y%m%d")), 0, province=this_province, genre=this_genre,
                                     business=title[0], url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                    if crawler.finderX(province_keywords, txt):  # 判断是否是重点省分项目
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('铁塔'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business=title[0],
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点省分重点项目 请注意')  # 判断是否是重点类型项目
                    else:
                        if crawler.finderX(business_keywords, txt):
                            crawler.save_xls('铁塔'+str(time.strftime("%y%m%d")), 1, genre=this_genre, province=this_province,
                                             business=title[0],
                                             url=temp_text, time=str(time.strftime("%Y-%m-%d")))
                            send_all(txt, '可能是重点项目 请注意')  # 判断是否是重点类型项目
    except Exception as err:
        crawler.log(err, 0)
    crawler.log("完成抓取，目前【铁塔】共抓取：" + str(len(chinatower_project_list)) + "条记录")

if __name__ == "__main__":
    second = sleeptime(0, 3, 0)
    tmp = sleeptime(0, 0, 10)
    crawler.log('系统启动', 0)
    flag = 0
    while True:
        try:
            seach_telecom_project()  # 电信
        except Exception as err:
            crawler.log('抓取电信项目出现问题,请检查网络连接')
            crawler.log(err, 0)

        try:
            seach_chinaunicom_project()  # 联通
        except Exception as err:
            crawler.log('抓取联通项目出现问题,请检查网络连接')
            crawler.log(err, 0)

        try:
            seach_chinamobile_project()  # 移动
        except Exception as err:
            crawler.log('抓取移动项目出现问题,请检查网络连接')
            crawler.log(err, 0)
        try:
            seach_chinatower_project()  # 铁塔
        except Exception as err:
            crawler.log('抓取铁塔项目出现问题,请检查网络连接')
            crawler.log(err, 0)

        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        crawler.log('三分钟后再次抓取信息')

        if int(time.strftime('%H')) > 22 and flag == 0:
            admin_mail.send_mail_with_file('统一抓取信息', '统一抓取信息')
            # sa_mail.send_mail_with_file('统一抓取信息', '统一抓取信息')
            flag = 1
        elif int(time.strftime('%H')) < 3 and flag == 1:
            flag = 0
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        time.sleep(second)
