# -*- coding: utf-8 -*-
"""
__author__ = 'Frank'
__mtime__ = '2017/12/27'
"""
from django.db import models
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class Log_dnspod_config(models.Model):
    TYPE = (
              (0,'增加'),
              (1,'修改'),
              (2,'删除'),
              (3,'切换'),
              (4, '禁用'),
              (5, '启用'),
              )
    op_user = models.CharField(max_length=50,verbose_name='操作用户',default=None)
    domain_name = models.CharField(max_length=100,verbose_name='域名',default=None)
    domain_record = models.CharField(max_length=100,default=None)
    op_type = models.IntegerField(choices=TYPE,verbose_name='操作类型')
    op_content = models.CharField(max_length=100, default=None, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'log_dnspod_operation'
        verbose_name = 'dnspod配置操作记录表'
        verbose_name_plural = 'dnspod配置操作记录表'

    def __unicode__(self):
        return self.op_user
