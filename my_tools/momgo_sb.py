#!/usr/bin/env python
# encoding: utf-8
import sys

import time

reload(sys)
sys.setdefaultencoding("utf-8")
import json

import pymongo

from my_tools.my_setting import TestDataDB

client = pymongo.MongoClient(host=TestDataDB.MONGODB_SERVER, port=TestDataDB.MONGODB_PORT)
db_auth = client.admin
db_auth.authenticate(TestDataDB.MONGO_USER, TestDataDB.MONGO_PSW)
db = client[TestDataDB.MONGODB_DB]
# a = db["bid_detail"].find(
#     {"_utime": {"$gte": "2017-09-05", "$lte": "2017-09-12"}, "_src.0.site": "www.chinabidding.com"},
#     no_cursor_timeout=True).count()
# cursor = db["bid_detail"].find(
#     {"_src.0.site": "www.chinabidding.com"},
#     no_cursor_timeout=True).sort([("_utime", -1)]).limit(10)
# with open("aaaa.txt", "w") as f:
#     for item in cursor:
#         item["_id"]=str(item["_id"])
#         # print item
#         f.write(json.dumps(item,ensure_ascii=False, indent=4))

# a = db["court_ktgg"].find({"_src.0.site": "ts.hncourt.gov.cn"}, no_cursor_timeout=True).count()
# b = db['bulletin'].find(
#     {"_src.0.site": "lnfy.chinacourt.org", "_src.0.url": "http://lnfy.chinacourt.org/public/detail.php?id=2359"},
#     no_cursor_timeout=True).count()
cur = db["judgement_wenshu"].find({}).limit(50000)
dict_a = None
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
dict_a = {"甘肃": 0, "兰州": 0, "嘉峪关": 0, "金昌": 0, "武威": 0, "酒泉": 0, "张掖": 0, "白银": 0, "平凉": 0, "庆阳": 0, "天水": 0,
          "陇南": 0, "临夏": 0, "甘南": 0}

for item in cur:
    for i in dict_a.keys():
        if i in item.get("case_name", "") or i in item.get("doc_content", ""):
            dict_a[i] += 1
print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
for k, v in dict_a.items():
    print k + ":", v

    # for i in ["甘肃", "兰州", "嘉峪关", "金昌", "武威", "酒泉", "张掖", "白银", "平凉", "庆阳", "天水", "陇南", "临夏", "甘南"]:
# print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     a = db["judgement_wenshu"].find({'$or': [{'case_name':
#                                                   {'$regex': ".*{}.*".format(i)}},
#                                              {"doc_content": {'$regex': ".*{}.*".format(i)}}]},
#                                     no_cursor_timeout=True).count()
#     print i + ":" + a
#     print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# a = db["environment_protection_information"].find({'$or': [{'company':
#                                                                 {'$regex': ".*{}.*".format("中航")}},
#                                                            {"company": {'$regex': ".*高科技.*"}}]},
#                                                   no_cursor_timeout=True).count()
# print a
# with open ("ssssb.txt","w") as f:
#     for item in b:
#         f.write
