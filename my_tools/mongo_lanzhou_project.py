#!/usr/bin/env python
# encoding: utf-8
import sys

import pymysql

sys.path.append('..')

reload(sys)
sys.setdefaultencoding("utf-8")
import time
from collections import OrderedDict
from common.loghandler import getLogger

import datetime
from xlwt import Workbook

from my_tools import my_email

import pymongo
from my_tools.my_setting import TestDataDB, tongji_mysql

HOST = tongji_mysql["host"]
USER = tongji_mysql["user"]
DATABASE = tongji_mysql["db"]
PASSWD = tongji_mysql["passwd"]
logger = getLogger("西北五省涉诉统计")
client = pymongo.MongoClient(host=TestDataDB.MONGODB_SERVER, port=TestDataDB.MONGODB_PORT)
db_auth = client.admin
db_auth.authenticate(TestDataDB.MONGO_USER, TestDataDB.MONGO_PSW)
db = client[TestDataDB.MONGODB_DB]

gansu = ("甘肃", "兰州", "嘉峪关", "金昌", "武威", "酒泉", "张掖", "白银", "平凉", "庆阳", "天水",
         "陇南", "临夏", "甘南")
xinjiang = ("新疆", "乌鲁木齐", "克拉玛依", "吐鲁番", "哈密", "阿克苏", "喀什", "昌吉",
            "博尔塔拉", "巴音郭楞", "克孜勒苏柯尔克孜", "伊犁", "和田")

qinghai = ("青海", "西宁", "海东市", "海北藏族自治州", "海南藏族自治州",
           "海西蒙古族藏族自治州", "黄南藏族自治州", "玉树", "果洛")

ningxia = ("宁夏", "银川", "石嘴山", "吴忠市", "固原", "中卫")

shanxi = ("陕西", "宝鸡", "咸阳", "渭南", "铜川", "西安", "汉中", "安康", "商洛", "榆林", "延安")


def wenshu(name_list):
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    dict_a = OrderedDict()
    for item in name_list:
        dict_a[item] = dict_all[item]

    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return dict_a


def ktgg(province):
    total = 0
    cur2 = db["court_ktgg"].find({})
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    for item in cur2:
        province2 = item.get("province", "")
        if item.get("province", "") is None:
            province2 = ""
        if province in province2:
            total += 1
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return total


def get_conn():
    conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, port=3306, db=DATABASE, charset='utf8')
    return conn


def main(name, wenshu_num, ktgg_num):
    sheet = w.add_sheet(name.decode("utf-8"))
    sheet.write(0, 0, "裁判文书".decode("utf-8"))
    sheet.write(1, 2, "{}数据增量".format(yesterday).decode("utf-8"))
    sheet.write(1, 0, "市".decode("utf-8"))
    sheet.write(1, 1, "{}数据量".format(datetime.date.today()).decode("utf-8"))
    start_index = 2

    ktgg_pk = "ktgg" + name + str(pre_yesterday)
    sql1 = "replace into involved_daily (province,date,topic,num,object) VALUES ('{}','{}','{}',{},'{}')".format(name,
                                                                                                                 yesterday,
                                                                                                                 "开庭公告",
                                                                                                                 ktgg_num,
                                                                                                                 ktgg_pk)
    excute(sql1)
    ctgg_inrease = get_increase(ktgg_num, ktgg_pk)
    for k, v in wenshu_num.items():
        wenshu_pk = k + str(pre_yesterday)
        wenshu_increase = get_increase(v, wenshu_pk)
        print wenshu_increase
        sheet.write(start_index, 0, k.decode("utf-8"))
        sheet.write(start_index, 1, v)
        sheet.write(start_index, 2, wenshu_increase)
        start_index += 1
        sql3 = "replace into involved_daily (province,date,topic,num,object) VALUES ('{}','{}','{}',{},'{}')".format(k,
                                                                                                                     yesterday,
                                                                                                                     "裁判文书",
                                                                                                                     v,
                                                                                                                     wenshu_pk)
        excute(sql3)
    sheet.write(start_index + 2, 0, "开庭公告数量".decode("utf-8"))
    sheet.write(start_index + 2, 1, ktgg_num)
    sheet.write(start_index + 2, 2, ctgg_inrease)


def get_increase(pre_num, pk):
    sql2 = "select num from involved_daily where object='{}'".format(pk)
    excute(sql2)
    try:
        pre_ctgg = mysql_cur.fetchone()[0]
    except:
        pre_ctgg = 0
    increase = pre_num - pre_ctgg
    return increase


def excute(sql):
    try:
        mysql_cur.execute(sql)
        logger.info(sql)
    except Exception as e:
        print sql, e
        logger.exception(e)
    mysql_db.commit()


def get_all_ktgg():
    cur = db["judgement_wenshu"].find({})
    for doc in cur:
        for city_ in all_city:
            if city_ in doc.get("case_name", "") or city_ in doc.get("doc_content", ""):
                dict_all[city] += 1


if __name__ == "__main__":
    w = Workbook()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    pre_yesterday = yesterday - datetime.timedelta(days=1)
    all_city = gansu + xinjiang + qinghai + ningxia + shanxi
    dict_all = {}
    for city in all_city:
        dict_all[city] = 0
    get_all_ktgg()
    dict_b = OrderedDict()
    dict_b["甘肃"] = gansu
    dict_b["新疆"] = xinjiang
    dict_b["青海"] = qinghai
    dict_b["宁夏"] = ningxia
    dict_b["陕西"] = shanxi
    mysql_db = get_conn()
    mysql_cur = mysql_db.cursor()
    for a, b in dict_b.items():
        print a
        ktgg_ = ktgg(a)
        wenshu_ = wenshu(b)
        main(a, wenshu_, ktgg_)
    w.save("5province_increase-{}.xls".format(yesterday))
    my_email.hz_send("兰州项目西北五省涉诉站点统计-{}".format(yesterday),
                     "5province_increase-{}.xls".decode("utf8").format(yesterday),
                     "tangxin@haizhi.com")
    mysql_db.close()
