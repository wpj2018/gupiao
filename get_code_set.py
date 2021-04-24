import urllib
import urllib.request
import re
import os


# 爬虫抓取网页函数
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html


# 获取所有的股票编号，正则表达式带（）时，返回值只包含括号里内容，即股票编号数组
def getStackCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    print(code)
    return code


Url = 'http://quote.eastmoney.com/stock_list.html'  # 东方财富网股票网址
filepath = 'D:\\data\\python\\stock\\'  # 定义数据文件保存路径
# 进行抓取
code = getStackCode(getHtml(Url))
# 获取所有以6开头的股票代码的集合
CodeList = []
for item in code:
    CodeList.append(item)
# 将网页上文件下载并保存到本地csv文件，注意日期
print(len(CodeList))