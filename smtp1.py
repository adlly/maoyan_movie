#-*-coding:UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

smtp_host='smtp.mxhichina.com'
smtp_port=25
smtp_user='hello@ifnot.cc'
smtp_pass='jie00.123'

sender=smtp_user
receivers=['hello@ifnot.cc','403324737@qq.com']

message = MIMEText('喵喵,么么哒~')
message['From'] = Header('小甜甜','utf-8')
message['To'] = Header('小笨笨','utf-8')

subject = 'python smtp send e-mails'
message['Subject']=Header(subject,'utf-8')

try:
    smtp_server = smtplib.SMTP()
    smtp_server.connect(smtp_host, smtp_port)
    smtp_server.login(smtp_user,smtp_pass)
    smtp_server.sendmail(sender,receivers,message.as_string())

except smtplib.SMTPException:
    print("Error: can't send e-mails")