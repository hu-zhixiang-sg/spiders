import smtplib
import ssl

def send_email(spider_name='',
               smtp_server='smtp.gmail.com',
               port=587,
               sender_email='test.spider.666@gmail.com',
               password='qwerasdf666',
               receiver_email='zhixiang.hu.ruc@gmail.com',
               message=''):
    if spider_name:
        message = f"Something is wrong with {spider_name} spider. Re-run it."

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)