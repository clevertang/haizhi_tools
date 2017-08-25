#!/usr/bin/env python
# encoding: utf-8
import os
import subprocess

import sys


# def run_cmd(cmd):
#     p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     while True:
#         line = p.stdout.readline()
#         if line:
#             sys.stdout.flush()
#         else:
#             break
#     p.wait()
# run_cmd("cd {}".format(os.getcwd()))
# run_cmd("python a.py")
from email.mime.multipart import MIMEMultipart


class Email(object):
    def send_email(self):
        pass
    def main(self):
        pass


if __name__ == "__main__":
    email = Email()
    email.send_email()


# 邮件对象:
msg = MIMEMultipart()
msg['From'] = _format_addr(u'Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8').encode()

# 邮件正文是MIMEText:
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))

# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open('/Users/michael/Downloads/test.png', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型:
    mime = MIMEBase('image', 'png', filename='test.png')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='test.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)