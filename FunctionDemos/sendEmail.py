import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 配置信息
smtp_server = 'smtp.exmail.qq.com'  # SMTP 服务器
smtp_port = 465  # SSL 端口
sender_email = ibkrconfig.sender_email  # 您的企业邮箱地址
password = ibkrconfig.password  # 步骤 1 中生成的客户端专用密码
receiver_email = ibkrconfig.sender_email  # 收件人邮箱
cc_email = ''  # 抄送人（可选，可为空）

# 邮件内容
subject = '定时任务'
body = '已触发任务执行，请及时关注'

# 构造邮件
message = MIMEText(body, 'plain', 'utf-8')
message['Subject'] = Header(subject, 'utf-8')
message['From'] = Header(sender_email, 'utf-8')
message['To'] = Header(receiver_email, 'utf-8')
if cc_email:
    message['Cc'] = Header(cc_email, 'utf-8')

# 发送邮件
try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(sender_email, password)
    # 发送给收件人和抄送人
    recipients = [receiver_email]
    if cc_email:
        recipients.append(cc_email)
    server.sendmail(sender_email, recipients, message.as_string())
    print("邮件发送成功！")
except Exception as e:
    print(f"邮件发送失败：{e}")
finally:
    server.quit()