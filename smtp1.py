
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#  这是定义几个需要使用的变量
smtp_host='smtp.mxhichina.com'
smtp_port=25
smtp_user='hello@ifnot.cc'
smtp_pass='jie00.123'

sender=smtp_user # 邮件发送者
receivers = ['mm@ifnot.cc', '403324737@qq.com']# 邮件接受者们

message = MIMEText('测试邮件！！！')
message['From'] = Header('你好', 'utf-8')
message['To'] = Header('这是测试', 'utf-8')

subject = 'python smtp 发送邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtp_server = smtplib.SMTP()
    smtp_server.connect(smtp_host, smtp_port)
    smtp_server.login(smtp_user, smtp_pass)
    smtp_server.sendmail(sender, receivers, message.as_string())
except smtplib.SMTPException:
    print("Error: 无法发送邮件")