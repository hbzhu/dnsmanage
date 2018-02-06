# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'JS01228Z'
__mtime__ = '2017/10/31'
"""
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser,Group
import time

class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('SU', 'SuperUser'),
        ('GA', 'GroupAdmin'),
        ('CU', 'CommonUser'),
    )
    name = models.CharField(max_length=80)
    role = models.CharField(max_length=2, choices=USER_ROLE_CHOICES, default='CU')

    class Meta:
        permissions = (
            ("can_read_user","查看user权限"),
            ("can_change_user", "更改user权限"),
            ("can_add_user", "添加user权限"),
            ("can_del_user", "删除user权限"),
        )
        verbose_name = "用户表"
        verbose_name_plural = "用户表"



    def __unicode__(self):
        return self.username





class Logs(models.Model):
    FLAG = (
              (0,'组'),
              (1,'用户'),
              )
    TYPE = (
              (0,'增加'),
              (1,'修改'),
              (2,'删除'),
              )

    op_user = models.CharField(max_length=50, verbose_name='操作用户', default=None)
    op_flag = models.IntegerField(choices=FLAG,verbose_name='操作标识')
    op_type = models.IntegerField(choices=TYPE,verbose_name='操作类型')
    op_content = models.CharField(max_length=100, default=None, blank=True, null=True,verbose_name='操作内容')
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='执行时间')

    class Meta:
        db_table = 'accounts_logs'
        verbose_name = '用户信息操作记录表'
        verbose_name_plural = '用户信息操作记录表'



