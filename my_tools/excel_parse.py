#!/usr/bin/env python
# encoding: utf-8
# -*- coding:UTF-8 -*-
import os
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


import xlrd

zhaohang = {
    "工商信息": [3, 33], "开庭公告": [34, 119], "裁判文书": [120, 149], "法院公告": [150, 151],
    "被执行人": [152, 173], "失信": [174, 174],
    "审判流程": [175, 179], "欠税信息": [180, 188], "行政处罚信息": [189, 220],
    "专利信息": [221, 221], "招标信息": [222, 282],
    "上市公司基本信息": [283, 283], "上市公告信息": [284, 284], "上市公司财报": [285, 288],
    "百度新闻": [289, 290], "新闻": [291, 322]
}


haizhi = {
    "工商信息": [3, 33], "开庭公告": [235, 321], "裁判文书": [114, 143], "法院公告": [233, 234],
    "被执行人": [144, 165], "失信": [166, 166],
    "审判流程": [167, 171], "欠税信息": [34, 42], "行政处罚信息": [43, 74],
    "专利信息": [75, 75], "招标信息": [172, 232],
    "上市公司基本信息": [110, 110], "上市公告信息": [109, 109], "上市公司财报": [111, 113],
    "百度新闻": [76, 76], "新闻": [77, 108],
}


def get_list1(name):
    start=zhaohang.get(name)[0]-1
    end=zhaohang.get(name)[1]

    list1 = []
    for i in range(start, end):
        row_data = sh1.row_values(i)
        s = row_data[11]
        # if s == "":
        host = row_data[8]
        try:
            s = re.findall(r"http://(.*?)/", host)[0]
        except:
            s=host
        list1.append(s)
    return list1


def get_list2(name):
    start = haizhi.get(name)[0]-1
    end = haizhi.get(name)[1]
    list2 = []
    for i in range(start, end):
        row_data = sh2.row_values(i)
        s = row_data[1]
        list2.append(s)
    return list2
    pass


def compare(name):
    list1 = get_list1(name)
    list2 = get_list2(name)
    f = open("{}.txt".format(name), "w")
    for i in list2:
        if i not in list1:
            f.write("more"+i + "\n")
    for j in list1:
        if j not in list2:
            f.write("lack"+j+"\n")
    f.close

if __name__ == "__main__":
    try:
        excel = xlrd.open_workbook("1.xlsx")
    except Exception as e:
        print "打开失败"
    sh1 = excel.sheet_by_name(u"迭代一")
    try:
        excel = xlrd.open_workbook("2.xls")
    except Exception as e:
        print "打开失败"
    sh2 = excel.sheet_by_name("Sheet1")
    for i in haizhi.keys():
        compare(i)
    # for i in []
