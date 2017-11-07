# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     enterprise_mysql
   Description :
   Author :       tangxin
   date：          2017/10/30
-------------------------------------------------
   Change Activity:
                   2017/10/30:
-------------------------------------------------
"""
import datetime
import pymongo
import pymysql
import sys
import time

sys.path.append('..')
from my_tools.my_setting import tongji_mysql, TestDataDB

from common.loghandler import getLogger

reload(sys)
sys.setdefaultencoding("utf-8")
logger = getLogger("工商统计")
HOST = tongji_mysql["host"]
USER = tongji_mysql["user"]
DATABASE = tongji_mysql["db"]
PASSWD = tongji_mysql["passwd"]

PROVINCES = ["安徽", "北京", "重庆", "福建", "广东", "甘肃", "广西", "贵州", "河南", "湖北", "河北",
             "海南", "黑龙江", "湖南", "吉林", "江苏", "江西", "辽宁", "内蒙古", "宁夏", "青海",
             "四川", "山东", "上海", "陕西", "山西", "天津", "新疆", "西藏", "云南",
             "浙江", ""]


def get_start(days):
    weekday = datetime.datetime.now().weekday()
    days = days + weekday
    today = datetime.date.today()
    length_days = datetime.timedelta(days=days)
    start = today - length_days
    return start


def get_mysql():
    # conn = pymysql.connect(host="localhost", user='root', passwd='tx123321z', port=3306, db="clevertang",
    #                        charset='utf8')
    conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, port=3306, db=DATABASE, charset='utf8')
    return conn


def get_mongo():
    client = pymongo.MongoClient(host=TestDataDB.MONGODB_SERVER, port=TestDataDB.MONGODB_PORT)
    db_auth = client.admin
    db_auth.authenticate(TestDataDB.MONGO_USER, TestDataDB.MONGO_PSW)
    db = client[TestDataDB.MONGODB_DB]
    return db


def excute(cur, sql):
    try:
        cur.execute(sql)
        logger.info(sql)
        print sql
    except Exception as e:
        logger.error("执行sql语句出错")
        logger.exception(e)


def main(province):
    this_week_registed_num = conn["enterprise_data_gov"].find(
        {"_in_time": {"$gt": start, "$lt": end}, "registered_date": {"$gt": middle, "$lt": end},
         "province": {'$regex': ".*{}.*".format(province)}},
        no_cursor_timeout=True).count()
    last_week_registed_num = conn["enterprise_data_gov"].find(
        {"_in_time": {"$gt": start, "$lt": end}, "registered_date": {"$gt": start, "$lt": middle},
         "province": {'$regex': ".*{}.*".format(province)}},
        no_cursor_timeout=True).count()
    utime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    ctime1 = get_ctime(cur, start, utime)
    ctime2 = get_ctime(cur, start, utime)
    if province == "":
        province = "全国"
    sql1 = "replace into enterprise_new_registered_company (id,registered_start,registered_num,ctime,utime,registered_end,province)" \
           "VALUES('{}','{}','{}','{}','{}','{}','{}')".format(start + province, start,
                                                               last_week_registed_num,
                                                               ctime1, utime,
                                                               dbmiddle,
                                                               province, )

    sql2 = "replace into enterprise_new_registered_company (id,registered_start,registered_num,ctime,utime,registered_end,province)" \
           "VALUES('{}','{}','{}','{}','{}','{}','{}')".format(middle + province, middle,
                                                               this_week_registed_num,
                                                               ctime2, utime, dbend,
                                                               province,
                                                               )
    excute(cur, sql1)
    excute(cur, sql2)
    mysqldb.commit()
    # mysqldb.close()


def get_ctime(cur, date, utime):
    try:
        cur.execute("select ctime from enterprise_new_registered_company where registered_start='{}'".format(date))
        ctime = cur.fetchone()[0]
    except:
        ctime = utime
    return ctime


if __name__ == "__main__":
    start = str(get_start(14))
    middle = str(get_start(7))
    end = str(datetime.date.today())
    dbend = str(get_start(0) - datetime.timedelta(days=1))
    dbmiddle = str(get_start(7) - datetime.timedelta(days=1))
    conn = get_mongo()
    mysqldb = get_mysql()
    cur = mysqldb.cursor()
    for province in PROVINCES:
        main(province)
    mysqldb.close()
