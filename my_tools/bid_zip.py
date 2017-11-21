# -*- coding:UTF-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     bid_zip
   Description :
   Author :       tangxin
   date：          2017/11/10
-------------------------------------------------
   Change Activity:
                   2017/11/10:
-------------------------------------------------
"""

import json
import sys

import datetime
import pymongo
import zipfile

sys.path.append("..")
sys.path.append("../..")
from common.loghandler import getLogger

from my_tools import my_email

reload(sys)
sys.setdefaultencoding('utf8')


class GsCredit:
    def __init__(self):
        pass

    @staticmethod
    def start():
        time = datetime.date.today()
        step_time = datetime.timedelta(days=1)
        time = time - step_time
        time1 = time - step_time
        tables = [
            "bid_detail"
        ]
        db_save = pymongo.MongoClient('172.16.215.16', 40042)['app_data']
        db_save.authenticate('work', 'haizhi')
        filename = '{0}.txt'.format('bid_detail--' + str(time) + '--' + str(time1))
        for table in tables:
            _file = open(filename, 'w')
            cursor = db_save[table].find(
                {"_in_time": {"$gte": "{}".format(time1), "$lte": "{}".format(time)}}, no_cursor_timeout=True)
            for element in cursor:
                try:
                    data = {
                        "bid_content": element.get("bid_content", ""),
                        "_src": element.get("_src", ""),
                        "title": element.get("title", ""),
                        "province": element.get("province", "")
                    }
                    _file.write(json.dumps(data, ensure_ascii=False) + "\n")
                except Exception, e:
                    logger.error(e)
            _file.close()
        z = zipfile.ZipFile(filename.replace("txt", "zip"), 'w', zipfile.ZIP_DEFLATED)
        z.write(filename)
        z.close()
        # my_email.qq_send("招标信息-{}".format(date), "招标信息-{}".format(date), filename.replace("txt", "zip"),
        #                  "tangxin@haizhi.com")
        logger.info("文件{}创建完成".format(filename))
        my_email.hz_send("招标信息-{}".format(date), filename.replace("txt", "zip"),
                         "tangxin@haizhi.com,hubo@haizhi.com,zhaobiao@xingheng.ai ")


if __name__ == "__main__":
    logger = getLogger("招中标导出")
    date = datetime.date.today()
    logger.info("开始{}".format(date))
    worker = GsCredit()
    worker.start()
    logger.info("完成{}".format(date))
