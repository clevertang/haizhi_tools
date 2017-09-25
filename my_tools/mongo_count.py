#!/usr/bin/env python
# encoding: utf-8

import datetime
import pymongo
import sys
import xlrd
import xlwt

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
from my_tools.my_setting import TestDataDB, mylogger


def get_start(days):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=days)
    start = today - oneday
    return str(start)


def main():
    days = 1
    try:
        days = int(sys.argv[1])
        print "查询时间为最近:" + sys.argv[1] + "天"
    except:
        pass
    #
    logger = mylogger(sys.path[0] + "/log.log")
    excel_file = xlwt.Workbook()
    table = excel_file.add_sheet('info', cell_overwrite_ok=True)
    client = pymongo.MongoClient(host=TestDataDB.MONGODB_SERVER, port=TestDataDB.MONGODB_PORT)
    db_auth = client.admin
    db_auth.authenticate(TestDataDB.MONGO_USER, TestDataDB.MONGO_PSW)
    db = client[TestDataDB.MONGODB_DB]
    excel = None
    try:
        excel = xlrd.open_workbook("count.xlsx")
    except Exception as e:
        logger.error("打开失败")
        logger.exception(e)
    sh = excel.sheet_by_index(0)
    rows = sh.nrows
    start = get_start(days)
    end = str(datetime.date.today())
    table.write(1, 0, "site_name")
    table.write(1, 1, "_in_time")
    table.write(1, 2, "_utime")

    for i in xrange(2, rows):
        row_data = sh.row_values(i)
        dbname = row_data[0]
        site = row_data[1]
        user = row_data[3]

        increase = db[dbname].find({"_in_time": {"$gte": start, "$lt": end}, "_src.0.site": site},
                                   no_cursor_timeout=True).count()
        update = db[dbname].find({"_utime": {"$gte": start, "$lt": end}, "_src.0.site": site},
                                 no_cursor_timeout=True).count()

        table.write(i, 0, site)
        table.write(i, 1, increase)
        table.write(i, 2, update)
        # table.write(i, 3, user)
        print i, site, increase, update
    excel_file.save("result.xls")
    print "完成"


if __name__ == "__main__":
    main()
