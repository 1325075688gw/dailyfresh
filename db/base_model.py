# 作者     ：gw
# 创建日期 ：2019-08-25  下午 13:25
# 文件名   ：base_model.py

from django.db import models

class BaseModel(models.Model):
    '''抽象模型基类'''
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        abstract = True