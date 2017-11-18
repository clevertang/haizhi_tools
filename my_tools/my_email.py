# encoding: utf-8
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import datetime
import sys

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
from my_tools import my_setting

_user = my_setting.email_setting["fromaddress"]
_pwd = my_setting.email_setting["frompassword"]


def hz_send(topic, name, _to):
    msg = MIMEMultipart()
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg["Subject"] = Header(topic, 'utf-8')
    msg["From"] = _user
    msg["To"] = _to
    part = MIMEText(topic, "utf-8")
    msg.attach(part)

    # ---这是附件部分---
    # xlsx类型附件
    part = MIMEApplication(open(name, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=name.encode("gb2312"))
    msg.attach(part)

    try:
        s = smtplib.SMTP_SSL("smtp.weibangong.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to.split(","), msg.as_string())
        s.quit()
        print "Success!"
    except smtplib.SMTPException, e:
        print "Falied,%s" % e


def qq_send(topic, subject, filename, _to):
    msg = MIMEMultipart()
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg["Subject"] = Header(subject, 'utf-8')
    msg["From"] = "961577196@qq.com"
    msg["To"] = _to
    part = MIMEText(topic, "utf-8")
    msg.attach(part)

    # ---这是附件部分---
    # xlsx类型附件
    part = MIMEApplication(open(filename, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=filename.encode("gb2312"))
    msg.attach(part)

    try:
        s = smtplib.SMTP_SSL(my_setting.email_setting_qq["server"], 465)
        s.login(my_setting.email_setting_qq["addr"], my_setting.email_setting_qq["passwd"])
        s.sendmail("961577196@qq.com", _to.split(","), msg.as_string())
        s.quit()
        print "Success!"
    except smtplib.SMTPException, e:
        print "Falied,%s" % e


if __name__ == "__main__":
    pass
    # pass
    # hz_send("火车采集器统计情况", '火车采集器{}数据统计.xls'.format(datetime.date.today()).decode("utf-8"), hubo)
    # send("招行站点统计情况", "result.xls", youfeng)
