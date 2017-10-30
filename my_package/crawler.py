import os
import re
import time
import xlrd
import shutil
from xlutils.copy import copy
import configparser

def log(txt, show = 1): # 日志系统
    txt_name = str('log/' + time.strftime("%y%m%d")) + "log.txt"
    if show:
        print(str(txt))
    with open(txt_name, 'a+')as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' # ' + str(txt) + '\n')



class my_conf(object):
    def __init__(self):
        self.getdata_conf = configparser.ConfigParser()
        #self.email_conf = configparser.ConfigParser()
        self.getdata_conf.read(r'conf/getdata.conf')
        #self.email_conf.read(r'conf\email.conf')

    def get_conf(self, section, option):
        return self.getdata_conf.get(section, option)

    def get_province_keywords(self):
        province_keywords = self.get_conf('business', 'province_keywords')
        province_keywords = province_keywords.split(',')
        return province_keywords

    def get_all_province_keywords(self):
        all_province_keywords = self.get_conf('business', 'all_province_keywords')
        all_province_keywords = all_province_keywords.split(',')
        return all_province_keywords

    def get_business_keywords(self):
        business_keywords = self.get_conf('business', 'business_keywords')
        business_keywords = business_keywords.split(',')
        return business_keywords

def finderX(key_words, string):
    #扫描内容是否含有指定关键字
    for value in key_words:
        regex = re.compile(value)  # 匹配关键字
        match = regex.search(string)
        if match:
            return value


def save_xls(file_name, sheet=0, province='', business='', genre='', url='', time='',status='', remarks=''):
    try:
        if not os.path.exists(file_name+".xls"):#查看是否已经存在excel文件,如果不存在则创建文件
            shutil.copy('templet/excel_templet.xls', file_name+".xls")
        file_name = file_name + ".xls"
        oldWb = xlrd.open_workbook(file_name, formatting_info=True)
    except Exception as err:
        log("excel文件打开出现故障")
        log(err, 0)

    try:
        oldWbS1 = oldWb.sheet_by_index(sheet)
        newWb = copy(oldWb)
        newWs1 = newWb.get_sheet(sheet)
        inserRowNo1 = 1
        newWs1.write(inserRowNo1, 0, province)
        newWs1.write(inserRowNo1, 1, business)
        newWs1.write(inserRowNo1, 2, genre)
        newWs1.write(inserRowNo1, 3, url)
        newWs1.write(inserRowNo1, 4, time)
        newWs1.write(inserRowNo1, 5, status)
        newWs1.write(inserRowNo1, 6, remarks)

        for rowIndex in range(inserRowNo1, oldWbS1.nrows):
            for colIndex in range(oldWbS1.ncols):
                newWs1.write(rowIndex + 1, colIndex, oldWbS1.cell(rowIndex, colIndex).value)
    except Exception as err:
        log("excel模板文件异常")
        log(err, 0)

    try:
        newWb.save(file_name)
        log("excel已更新并保存最新的内容", 0)
    except Exception as err:
        log("excel文件保存出现异常")
        log(err, 0)


