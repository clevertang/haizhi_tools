# encoding: utf-8
import smtplib
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
youfeng = my_setting.email_setting["toaddress1"]
hubo = my_setting.email_setting["toaddress2"]


def send(topic, name, _to):
    msg = MIMEMultipart()
    msg["Subject"] = str(datetime.date.today())
    msg["From"] = _user
    msg["To"] = _to
    part = MIMEText(topic, "utf-8")
    msg.attach(part)

    # ---这是附件部分---
    # xlsx类型附件
    part = MIMEApplication(open(name, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=name)
    msg.attach(part)

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        print "Success!"
    except smtplib.SMTPException, e:
        print "Falied,%s" % e


if __name__=="__main__":
    send("火车采集器统计情况","huoche.xls",hubo)
    send("招行站点统计情况","result.xls",youfeng)