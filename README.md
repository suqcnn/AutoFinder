# AutoFinder
网络爬虫获取招标信息

Python版本：python 3.5
依赖包：
selenium
re
urllib
xlrd
shutil
xlutils.copy
configparser
 
 
文件目录及说明：
AutoFinder_2.3F
├── conf  ←此目录可不使用（此版本未配置conf）
│   ├── business.conf
│   ├── email.conf
│   ├── getdata.conf
│   └── getdata.txt
├── get_data.py ←主文件
├── ghostdriver.log ←浏览器日志
├── log ←日志目录（记录每天的运行情况，文件名示例 如下）
│   └── 170912log.txt
├── my_package
│   ├── crawler.py ←方法集中处理类
│   ├── __init__.py
│   ├── pemail.py ←邮件处理类
│   └── __pycache__
│       ├── crawler.cpython-35.pyc
│       ├── __init__.cpython-35.pyc
│       └── pemail.cpython-35.pyc
├── nohup.out ←运行输出（可配合日志使用）
├── templet
   └── excel_templet.xls ←excel模板文件
 
 
部署及使用：
Copy AutoFinder文件夹到工作目录
Copy phantomjs文件到工作目录（可直接在官网下载,由于移动招标网采用反爬虫异步加载，不部署此文件会影响移动数据抓取）
运行命令 python3 getdata.py
#隐式加载nohup -u python3 getdata.py &
