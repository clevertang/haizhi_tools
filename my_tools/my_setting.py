#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2017/7/12 上午11:22
@Author: CZC
@File: config.py
"""
import logging

mysql_setting = {
    "host": "rm-wz9x07x9567465305.mysql.rds.aliyuncs.com",
    "port": "3306",
    "db": 'cmb_crawl',
    "user": 'work',
    "passwd": 'haizhi@)3'
}

email_setting = {
    "fromaddress": "tangxin@haizhi.com",
    "frompassword": "tx123321z",
    "toaddress1": "youfeng@haizhi.com,zhangjun@haizhi.com,tangxin@haizhi.com",
    "toaddress2": "hubo@haizhi.com,zhangjun@haizhi.com,tangxin@haizhi.com",
    "server": "smtp.qq.com"

}


class TestDataDB(object):
    MONGODB_SERVER = "172.16.215.16"
    MONGODB_PORT = 40042
    MONGODB_DB = "app_data"
    MONGO_USER = "work"
    MONGO_PSW = "haizhi"

    MONGODB_COLLECTION = "gdebidding0821"
    MONGODB_COLLECTION2 = "landchina"
    MONGODB_COLLECTION3 = "landchina0821_tangxin"
    MONGODB_COLLECTION0819 = "landchina0819"


def mylogger(log_path):
    logger = logging.getLogger("root")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_path)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


BEANSTALK_HOST = 'cs2'
BEANSTALK_PORT = 11300
BEANSTALK_TUBE = 'offline_extract_info'
