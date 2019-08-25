# 作者     ：gw
# 创建日期 ：2019-08-25  下午 16:37
# 文件名   ：tasks.py
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time



app = Celery('celery_tasks/tasks', broker='redis://127.0.0.1:6379/1')

@app.task
def send_email(receiver, username, token):
    subject = '天天生鲜'
    message = ''
    html_message = '<h1>{0},欢迎您注册成为天天生鲜用户!<h1/><br/>请点击以下链接激活用户<a href="http:127.0.0.1:8000/user/active/{1}">http:127.0.0.1:8000/user/active/{1}<a/>'.format(
        username, token)
    receive_list = [receiver]
    sender = settings.EMAIL_FROM
    time.sleep(5)
    send_mail(subject=subject, message=message, from_email=sender, recipient_list=receive_list,
              html_message=html_message)
