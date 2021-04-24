#coding:utf-8
from os import listdir
from chardet import detect
import threading
import pymysql
import codecs
import json
import time
from datetime import datetime, date, timedelta
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


def creat_year_tb(table_name, database='gupiao'):
    colum = "date_time varchar(255),code varchar(255),name varchar(255),price_end varchar(255),price_max varchar(255),price_min varchar(255),price_start varchar(255),price_end_1 varchar(255),price_inc_val varchar(255),price_inc_rate varchar(255),ex_rate varchar(255),cj_num varchar(255),cj_sum varchar(255),sum varchar(255),lt_sum varchar(255)"
    create_sql = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'

    # 使用数据库
    cur.execute('use %s' % database)
    # 设置编码格式
    cur.execute('SET NAMES utf8;')
    cur.execute('SET character_set_connection=utf8;')
    # 执行create_sql，创建表

    cur.execute(create_sql)
    # 执行data_sql，导入数据
    conn.commit()

    cmd = "select * from tb_gp_org where date_time >= '2018-01-01' and date_time <='2020-05-10'"
    cur.execute(cmd)
    result = cur.fetchall()
    for elem in result:
        cmd = "insert into tb_gp_year2 values " + str(elem)
        cur.execute(cmd)
        conn.commit()

    # 关闭连接
    conn.close()
    cur.close()


def save_dic(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=True)


def load_dic(filename):
    with open(filename, "r") as json_file:
        dic = json.load(json_file)
    return dic


def pre_date(date):
    pre = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=-1)  # 昨天日期
    return pre.strftime("%Y-%m-%d")


def next_date(date):
    next = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)  # 昨天日期
    return next.strftime("%Y-%m-%d")


def search(database='gupiao'):
    gp_dic = {}
    '''
    # 使用数据库
    cur.execute('use %s' % database)

    cmd = "select code, name, price_inc_rate, date_time from tb_gp_year2 where date_time >= '2018-01-01' and date_time <='2020-05-10'"
    cur.execute(cmd)
    result = cur.fetchall()
    for elem in result:
        code, _, rate, date_time = elem
        if date_time not in gp_dic:
            gp_dic[date_time] = {}
        if code not in gp_dic[date_time]:
            gp_dic[date_time][code] = rate
    save_dic('gp.json', gp_dic)
    '''
    gp_dic = load_dic('gp.json')
    date = '2019-01-01'
    res = {}

    while date < '2020-05-10':
        if date not in gp_dic:
            date = next_date(date)
            continue

        count = {}
        zt_count = 0
        for code in gp_dic[date]:
            if gp_dic[date][code] == 'None' or float(gp_dic[date][code]) < 10:
                continue
            zt_count = zt_count + 1
            count[code] = 0
            cur = date

            while True:
                if cur in gp_dic:
                    if code not in gp_dic[cur] or gp_dic[cur][code] =='None' or float(gp_dic[cur][code]) < 10:
                        break
                    count[code] = count[code] + 1
                cur = pre_date(cur)

        res[date] = {}
        res[date]['max_lb'] = 0
        res[date]['zt_count'] = zt_count
        for i in range(1, 20):
            res[date]['lb_{}'.format(i)] = set()
        for key in count:
            lb_cnt = count[key]
            if lb_cnt > res[date]['max_lb']:
                res[date]['max_lb'] = lb_cnt
            res[date]['lb_{}'.format(lb_cnt)].add(key)

        date = next_date(date)

    date = '2019-01-01'
    while date < '2020-05-10':
        if date not in gp_dic:
            date = next_date(date)
            continue
        print(date, len(res[date]['lb_1']), res[date]['lb_1'])
        date = next_date(date)
#    print(total_lb_2, lb_success)

#creat_year_tb("tb_gp_year2")
search()