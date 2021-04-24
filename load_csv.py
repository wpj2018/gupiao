#coding:utf-8
from os import listdir
from chardet import detect
import threading
import pymysql
import codecs
import os

dic = {"日期": "date_time", "股票代码": "code", "名称":"name", "收盘价":"price_end", "最高价": "price_max",
       "最低价":"price_min", "开盘价": "price_start", "前收盘": "price_prev", "涨跌额":"price_val", "涨跌幅": "price_rate",
       "换手率":"ex_rate", "成交量": "cj_num", "成交金额":"cj_sum", "总市值":"sum", "流通市值":"lt_sum"}
# 连接数据库
config = {'host': '',
          'port': 3306,
          'user': 'root',
          'passwd': '',
          'charset': 'utf8mb4',
          'local_infile': 1
          }
conn = pymysql.connect(**config)
cur = conn.cursor()


def convert_csv(file):
    with open(file, 'rb+') as fp:
        content = fp.read()
        encoding = detect(content)['encoding']
        if encoding != 'utf-8':
            encoding = 'gbk'
        content = content.decode(encoding).replace('\'','').encode('utf8')
        fp.seek(0)
        fp.write(content)

# load_csv函数，参数分别为csv文件路径，表名称，数据库名称
def load_one_csv(csv_file_path, table_name, database='gupiao'):
    file = codecs.open(csv_file_path, 'rb', 'utf-8')
    reader = file.readline()
    b = reader.strip().split(',')
    colum = ''
    for a in b:
        colum = colum + dic[a] + ' varchar(255),'
    colum = colum[:-1]

    # 编写sql，create_sql负责创建表，data_sql负责导入数据
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'
    data_sql = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES" % (
        csv_file_path, table_name)
    # 使用数据库
    cur.execute('use %s' % database)
    # 设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 执行create_sql，创建表

    cur.execute(create_sql)
    # 执行data_sql，导入数据
    cur.execute(data_sql)
    conn.commit()

def convert():
    files = listdir("csv")
    num = len(files)
    for i in range(num):
        file = os.path.join("csv/", files[i])
        convert_csv(file)
        print("total:{} convert file {} success.".format(num, i))


def load_csv():
    err_f = open("error.txt", "w")

    files = listdir("csv")
    for i in range(len(files)):

        file = os.path.join("csv/", files[i])
        print(file)
        load_one_csv(file, "tb_gp", "gupiao")
        print("load {} success".format(file))
    # 关闭连接
    conn.close()
    cur.close()


#convert()
load_csv()