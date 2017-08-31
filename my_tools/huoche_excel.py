#!/usr/bin/env python
# encoding: utf-8
# 用来统计火车采集器的运行情况,对于正在运行的任务,可能出现获取的topic或其他为空值或为0的情况
# 在使用过程中发现任何bug,请联系唐新.


import json

import time

import datetime
from pyExcelerator import *

reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import logging


def get_count(url, session):
    try_count = 0
    while try_count < 3:
        try:
            try_count += 1
            resp = session.get(url)
            if resp.status_code != 200 or resp.text == "":
                logging.error("网络异常")
            return json.loads(resp.content)["Count"]
        except:
            pass
    return 0


def get_topic(url, session):
    try_count = 0
    while try_count < 3:
        try:
            try_count += 1
            resp = session.get(url)
            if resp.status_code != 200 or resp.text == "":
                print "出错,请重试"
            data = json.loads(resp.content)["Data"]
            return data[0]["topic"]
        except Exception as e:
            pass
    return ""


def main():
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    olds = None
    try:
        f = open("火车采集器辅助.txt")
        olds = f.readlines()
        f.close()
    except:
        print "欢迎第一次使用"
    finally:
        f = open("火车采集器辅助.txt", "w")
    w = Workbook()
    sheet1 = w.add_sheet('站点数据量统计'.decode("utf-8"))
    sheet2 = w.add_sheet("数据总览".decode("utf-8"))
    sheet1.write(0, 0, '站点'.decode("utf-8"))
    sheet1.write(0, 1, '主题'.decode("utf-8"))
    sheet1.write(0, 2, '数据量'.decode("utf-8"))
    sheet1.write(0, 3, '数据增量'.decode("utf-8"))
    sheet2.write(0, 0, "站点(模块)总数".decode("utf-8"))
    sheet2.write(1, 0, "昨日新增站点数".decode("utf-8"))
    sheet2.write(2, 0, "新闻站点总数".decode("utf-8"))
    sheet2.write(3, 0, "新闻数据量总数".decode("utf-8"))
    sheet2.write(4, 0, "新闻数据昨日新增数".decode("utf-8"))
    sheet2.write(5, 0, "裁判文书站点总数".decode("utf-8"))
    sheet2.write(6, 0, "裁判文书数据量总数".decode("utf-8"))
    sheet2.write(7, 0, "裁判文书昨日新增".decode("utf-8"))
    sheet2.write(8, 0, "招投标站点总数".decode("utf-8"))
    sheet2.write(9, 0, "招投标数据量总数".decode("utf-8"))
    sheet2.write(10, 0, "招投标昨日新增".decode("utf-8"))
    sheet2.write(11, 0, "异常站点".decode("utf-8"))

    session = requests.session()
    url = "http://182.61.40.11:808/api?&model=job&action=list&type=json"
    try_count = 0
    all_sites = None
    while try_count < 3:
        try:
            try_count += 1
            resp = session.get(url)
            if resp.status_code != 200 or resp.text == "":
                logging.error("网络异常")
            all_sites = json.loads(resp.content)["Data"]
            break
        except Exception as e:
            logging.exception(e)
    if try_count == 3:
        logging.info("程序退出")
        sys.exit()
    news_num = 0
    news_count = 0
    news_new = 0
    bid_num = 0
    bid_count = 0
    bid_new = 0
    wenshu_num = 0
    wenshu_count = 0
    wenshu_new = 0
    wrong = 0
    for i in xrange(0, len(all_sites)):
        task_id = all_sites[i]["JobId"]
        task_name = all_sites[i]["JobName"]
        count_url = "http://182.61.40.11:808/api?model=data&action=count&opreator=0&type=json&jobid={}".format(task_id)
        topic_url = "http://182.61.40.11:808/api?model=data&action=view&type=json&pn=0&rn=20&jobid={}".format(task_id)

        count = get_count(count_url, session)
        topic = get_topic(topic_url, session).replace('\r\n', '')

        sheet1.write(i + 1, 0, task_name.decode('utf-8'))
        sheet1.write(i + 1, 1, topic.decode('utf-8'))
        sheet1.write(i + 1, 2, str(count).decode('utf-8'))
        f.write(str(count) + "\n")
        try:
            old = olds[i]
        except:
            old = 0
        increase = count - int(old)
        sheet1.write(i + 1, 3, increase)
        if "news" in topic:
            news_num += 1
            news_count += count
            news_new += increase

        elif "wenshu" in topic:
            wenshu_num += 1
            wenshu_count += count
            wenshu_new += increase

        elif "bid" in topic:
            bid_num += 1
            bid_count += count
            bid_new += increase
        else:
            wrong += 1
    sheet2.write(0, 1, len(all_sites))
    sheet2.write(1, 1, len(all_sites) - len(olds))
    sheet2.write(2, 1, news_num)
    sheet2.write(3, 1, news_count)
    sheet2.write(4, 1, news_new)
    sheet2.write(5, 1, wenshu_num)
    sheet2.write(6, 1, wenshu_count)
    sheet2.write(7, 1, wenshu_new)
    sheet2.write(8, 1, bid_num)
    sheet2.write(9, 1, bid_count)
    sheet2.write(10, 1, bid_new)
    sheet2.write(11, 1, wrong)
    f.close()
    w.save('火车采集器{}数据统计.xls'.format(datetime.date.today()))
    print "文件创建完成"
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


if __name__ == "__main__":
    main()
