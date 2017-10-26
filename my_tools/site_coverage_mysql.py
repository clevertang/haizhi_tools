# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     site_coverage_mysql
   Description :
   Author :       tangxin
   date：          2017/10/25
-------------------------------------------------
   Change Activity:
                   2017/10/25:
-------------------------------------------------
"""
import time

import pymysql
import xlrd
import sys

sys.path.append('..')
from my_tools.my_setting import tongji_mysql

from common.loghandler import getLogger

reload(sys)
sys.setdefaultencoding("utf-8")
logger = getLogger("站点加权覆盖计算")
HOST = tongji_mysql["host"]
USER = tongji_mysql["user"]
DATABASE = tongji_mysql["db"]
PASSWD = tongji_mysql["passwd"]
name_list = ["工商站点", "招中标站点", "裁判文书站点", "开庭公告站点", "审判流程站点",
             "法院公告站点", "欠税公告站点", "失信被执行人站点", "被执行人站点", "行政处罚站点",
             "纳税等级站点", "新闻"]


class my_mysql(object):
    def get_conn(self):
        # conn = pymysql.connect(host=localhost, user='root', passwd='tx123321z', port=3306, db="clevertang",
        #                        charset='utf8')
        conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, port=3306, db=DATABASE, charset='utf8')
        return conn


class my_dict(object):
    def __init__(self):
        self.city = 0
        self.province = 0
        self.county = 0
        self.nation = 0
        self.all = 0
        self.jiaquan = 0

    def judge(self, num):
        if num == 1:
            self.county += 1
        if num == 8.54:
            self.city += 1
        if num == 83.85:
            self.province += 1
        if num == 2851:
            self.nation += 1
        self.all = self.nation + self.province + self.city + self.county
        self.jiaquan = self.county * 1 + self.city * 8.54 + self.province * 83.85 + self.nation * 2581


def parse_source():
    try:
        source = xlrd.open_workbook(
            "/Users/haizhi/clevertang/DataGroup-Docs/04产品与迭代/海致互联网数据采集系统/03_系统数据源/汇总文档/[2017-10-12]数据源调研列表.xlsm")
    except Exception as e:
        logger.error("数据源调研列表打开失败")
        logger.exception(e)
        sys.exit()

    source_table = source.sheet_by_index(0)
    source_rows = source_table.nrows
    gongshang = my_dict()
    bid = my_dict()
    judgement_wenshu = my_dict()
    ktgg = my_dict()
    judge_process = my_dict()
    bulletin = my_dict()
    enterprise_owing_tax = my_dict()
    shixin_info = my_dict()
    b_zhixing = my_dict()
    penalty = my_dict()
    tax = my_dict()
    news = my_dict()
    all_topics = []
    all_topics.append(gongshang)
    all_topics.append(bid)
    all_topics.append(judgement_wenshu)
    all_topics.append(ktgg)
    all_topics.append(judge_process)
    all_topics.append(bulletin)
    all_topics.append(enterprise_owing_tax)
    all_topics.append(shixin_info)
    all_topics.append(b_zhixing)
    all_topics.append(penalty)
    all_topics.append(tax)
    all_topics.append(news)
    for i in xrange(3, source_rows):
        row_data = source_table.row_values(i)
        if row_data[0] == u"工商信息":
            gongshang.judge(row_data[4])
        if u"招" in row_data[0] and u"标" in row_data[0]:
            bid.judge(row_data[4])
        if row_data[0] == u"裁判文书":
            judgement_wenshu.judge(row_data[4])
        if row_data[0] == u"开庭公告":
            ktgg.judge(row_data[4])
        if row_data[0] == u"审判流程":
            judge_process.judge(row_data[4])
        if row_data[0] == u"法院公告":
            bulletin.judge(row_data[4])
        if row_data[0] == u"欠税信息":
            enterprise_owing_tax.judge(row_data[4])
        if u"失信" in row_data[0]:
            shixin_info.judge(row_data[4])
        if row_data[0] == u"被执行人":
            b_zhixing.judge(row_data[4])
        if row_data[0] == u"行政处罚":
            penalty.judge(row_data[4])
        if row_data[0] == u"纳税等级":
            tax.judge(row_data[4])
        if row_data[0] == u"新闻":
            news.judge(row_data[4])
    return all_topics


def parse_real():
    try:
        real = xlrd.open_workbook(
            "/Users/haizhi/clevertang/DataGroup-Docs/04产品与迭代/海致互联网数据采集系统/03_系统数据源/汇总文档/[2017-10-12]已采集数据源列表.xlsm")
    except Exception as e:
        logger.error("已采集数据源列表打开失败")
        logger.exception(e)
        sys.exit()
    real_table = real.sheet_by_index(0)
    real_rows = real_table.nrows
    gongshang = my_dict()
    bid = my_dict()
    judgement_wenshu = my_dict()
    ktgg = my_dict()
    judge_process = my_dict()
    bulletin = my_dict()
    enterprise_owing_tax = my_dict()
    shixin_info = my_dict()
    b_zhixing = my_dict()
    penalty = my_dict()
    tax = my_dict()
    news = my_dict()
    all_topics = []
    all_topics.append(gongshang)
    all_topics.append(bid)
    all_topics.append(judgement_wenshu)
    all_topics.append(ktgg)
    all_topics.append(judge_process)
    all_topics.append(bulletin)
    all_topics.append(enterprise_owing_tax)
    all_topics.append(shixin_info)
    all_topics.append(b_zhixing)
    all_topics.append(penalty)
    all_topics.append(tax)
    all_topics.append(news)
    for i in xrange(0, real_rows):
        row_data = real_table.row_values(i)
        if row_data[0] == u"工商信息":
            gongshang.judge(row_data[5])
        if u"招" in row_data[0] and u"标" in row_data[0]:
            bid.judge(row_data[5])
        if row_data[0] == u"裁判文书":
            judgement_wenshu.judge(row_data[5])
        if row_data[0] == u"开庭公告":
            ktgg.judge(row_data[5])
        if row_data[0] == u"审判流程":
            judge_process.judge(row_data[5])
        if row_data[0] == u"法院公告":
            bulletin.judge(row_data[5])
        if row_data[0] == u"欠税信息":
            enterprise_owing_tax.judge(row_data[5])
        if u"失信" in row_data[0]:
            shixin_info.judge(row_data[5])
        if row_data[0] == u"被执行人":
            b_zhixing.judge(row_data[5])
        if row_data[0] == u"行政处罚":
            penalty.judge(row_data[5])
        if row_data[0] == u"纳税等级":
            tax.judge(row_data[5])
        if row_data[0] == u"新闻":
            news.judge(row_data[5])
    return all_topics


def get_CT(table):
    update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cur.execute("select ctime from {} where id={}".format(table, topic_id + 1))
    try:
        create_time = cur.fetchone()[0]
    except:
        create_time = update_time
    if create_time is None:
        create_time = update_time
    return create_time, update_time


def mysql_excute(sql):
    capture_list.append(source_result[topic_id].all)
    # try:
    print sql
    cur.execute(sql)
    logger.info(sql)
    # except Exception as e:
    #     logger.exception(e)
    db.commit()


def get_pre_investigate(topic_id):
    pre_investigate = 334 - source_result[topic_id].all
    if pre_investigate < 0:
        pre_investigate = 2851 - source_result[topic_id].all
        return pre_investigate, "县"
    if topic_id == 0:
        pre_investigate = 3
        return pre_investigate, "省"
    return pre_investigate, "市"


if __name__ == "__main__":
    source_result = parse_source()
    print "++++++++++++++"
    capture_result = parse_real()
    conn = my_mysql()
    db = conn.get_conn()
    cur = db.cursor()
    capture_list = []
    count_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    for topic_id in xrange(0, len(source_result)):
        s_nation = source_result[topic_id].nation
        s_province = source_result[topic_id].province
        s_city = source_result[topic_id].city
        s_county = source_result[topic_id].county
        r_nation = capture_result[topic_id].nation
        r_province = capture_result[topic_id].province
        r_city = capture_result[topic_id].city
        r_county = capture_result[topic_id].county
        pre_investigate, unit = get_pre_investigate(topic_id)
        try:
            coverage = capture_result[topic_id].jiaquan / source_result[topic_id].jiaquan
        except:
            coverage = 0
        topic_cn = name_list[topic_id]
        Inexistent_amount = 0
        Existent_captured_amount = capture_result[topic_id].all  # 已抓取总量
        Existent_pre_capture_amount = source_result[topic_id].all - Existent_captured_amount
        create_time1, update_time1 = get_CT('topic_coverage')
        sql1 = "replace INTO topic_coverage (id,topic_cn,Inexistent_amount,Existent_captured_amount," \
               "Existent_pre_capture_amount,utime,ctime,pre_investigate)" \
               " VALUES ({},'{}',{},{},{},'{}','{}',{})".format(
            topic_id + 1, topic_cn, Inexistent_amount, Existent_captured_amount, Existent_pre_capture_amount,
            update_time1, create_time1, pre_investigate)
        mysql_excute(sql1)
        create_time2, update_time2 = get_CT('weighted_coverage')
        sql2 = "replace into weighted_coverage (id,topic_cn,coverage,total_nation," \
               "actual_nation,total_province,actual_province," \
               "total_city,actual_city,total_county,actual_county,utime,ctime,unit)" \
               "VALUES({},'{}',{},{},{},{},{},{},{},{},{},'{}','{}','{}')".format(topic_id + 1, topic_cn,
                                                                                  coverage, s_nation, r_nation,
                                                                                  s_province,
                                                                                  r_province, s_city, r_city,
                                                                                  s_county, r_county, update_time2,
                                                                                  create_time2, unit)
        mysql_excute(sql2)
        create_time3, update_time3 = get_CT('topic_coverage_increase')
        sql3 = "insert INTO topic_coverage_increase (topic_cn,count_time,coverage," \
               "already_crawl,total_crawl,ctime,utime)" \
               " VALUES ('{}','{}',{},{},{},'{}','{}')".format(
            topic_cn, count_time, coverage, Existent_captured_amount,
            source_result[topic_id].all, update_time3, create_time3)
        mysql_excute(sql3)
        create_time4, update_time4 = get_CT('weighted_coverage_increase')

        sql4 = "insert into weighted_coverage_increase (count_time,topic_cn,coverage,total_nation," \
               "actual_nation,total_province,actual_province," \
               "total_city,actual_city,total_county,actual_county,utime,ctime,unit)" \
               "VALUES('{}','{}',{},{},{},{},{},{},{},{},{},'{}','{}','{}')".format(count_time, topic_cn,
                                                                                  coverage, s_nation, r_nation,
                                                                                  s_province,
                                                                                  r_province, s_city, r_city,
                                                                                  s_county, r_county, update_time4,
                                                                                  create_time4, unit)
        mysql_excute(sql4)
