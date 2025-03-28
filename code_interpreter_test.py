# import smtplib
# from email.message import EmailMessage
#
# sender_email = "2028433454@qq.com"
# password = "flwmdydxrlxuebbi"  # 这里应该使用 QQ 邮箱的授权码
#
# msg = EmailMessage()
# msg.set_content("This is the content of the email.")
# msg['Subject'] = "Test Subject"
# msg['From'] = sender_email
# msg['To'] = "1412189000@qq.com"
#
# # 使用 SSL 和 465 端口
# with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
#     server.login(sender_email, password)
#     server.send_message(msg)
from apscheduler.schedulers.blocking import BlockingScheduler
import time
def job_function():
    print("Hello from the scheduled job!")
    print(time.time())

scheduler = BlockingScheduler()
scheduler.add_job(job_function, 'interval', days=1, start_date='2023-10-21 21:37:00')
scheduler.start()

import yagmail

# 设置发件人邮箱和授权码
sender_email = "2028433454@qq.com"
password = "flwmdydxrlxuebbi"

# 创建 yagmail 客户端对象
yag = yagmail.SMTP(sender_email, password,host='smtp.qq.com')

# 发送邮件
yag.send(
    to="1412189000@qq.com",
    subject="Test Subject",
    contents="test"
)

# 关闭连接
yag.close()