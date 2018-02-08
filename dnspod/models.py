# -*- coding: utf-8 -*-
"""
__author__ = 'Frank'
__mtime__ = '2017/12/15'
"""
from __future__ import unicode_literals
from django.db import models


class Dnspod_domains(models.Model):
    domain_id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=64,blank=False,verbose_name=u'域名')

    def __unicode__(self):
        return self.domain

    class Meta:
        db_table = 'dnspod_domains'
        verbose_name = '域名表'
        verbose_name_plural = '域名表'
        permissions = (
            ("can_read_domains","查看domains权限"),
            ("can_change_domains", "更改domains权限"),
            ("can_add_domains", "添加domains权限"),
            ("can_del_domains", "删除domains权限"),
        )


class Dnspod_records(models.Model):
    record_id = models.IntegerField()
    client_ip = models.GenericIPAddressField(blank=True,null=True)
    record = models.CharField(max_length=64,blank=True, null=True, verbose_name=u'主机记录')
    record_type = models.CharField(max_length=64,verbose_name=u"类型")
    record_value = models.CharField(max_length=256,blank=True,verbose_name=u"记录值")
    record_line = models.CharField(max_length=64, verbose_name=u"线路",default="默认")
    domain_id = models.ForeignKey('Dnspod_domains')
    qcloud_record = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'qcloud_cname')
    upyun_record = models.CharField(max_length=64,blank=True,null=True,verbose_name=u'upyun_cname')
    source_record = models.CharField(max_length=64, blank=True,null=True,verbose_name=u'回源地址')
    update_time = models.DateTimeField(blank=True,null=True, verbose_name=u"更新时间")
    sync_time = models.DateTimeField(auto_now_add=True, verbose_name=u"同步时间")


    def __unicode__(self):
        return self.record

    class Meta:
        db_table = 'dnspod_records'
        verbose_name = '解析记录表'
        verbose_name_plural = '解析记录表'
        permissions = (
            ("can_read_dnspod_records","查看dnspod_records权限"),
            ("can_change_dnspod_records", "更改dnspod_records权限"),
            ("can_add_dnspod_records", "添加dnspod_records权限"),
            ("can_del_dnspod_records", "删除dnspod_records权限"),
        )



class Dnspod_cdnrecords(models.Model):
    full_domain = models.CharField(max_length=64,unique=True,verbose_name=u'加速域名')
    qcloud_record = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'qcloud_cname')
    upyun_record = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'upyun_cname')
    source_record = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'回源地址')
    sync_time = models.DateTimeField(auto_now_add=True, verbose_name=u"同步时间")

    def __unicode__(self):
        return self.full_domain


    class Meta:
        db_table = 'dnspod_cdnrecords'
        verbose_name = 'CDN记录表'
        verbose_name_plural = 'CDN记录表'
        permissions = (
            ("can_read_dnspod_cdnrecords","查看dnspod_cdnrecords权限"),
            ("can_change_dnspod_cdnrecords", "更改dnspod_cdnrecords权限"),
            ("can_add_dnspod_cdnrecords", "添加dnspod_cdnrecords权限"),
            ("can_del_dnspod_cdnrecords", "删除dnspod_cdnrecords权限"),
        )

class Dnspod_stat(models.Model):
    domain = models.CharField(max_length=64)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name=u"记录时间")
    record_count = models.IntegerField()

    def __unicode__(self):
        return self.domain

    class Meta:
        db_table = 'dnspod_stat'
        verbose_name = '记录汇总表'
        verbose_name_plural = '记录汇总表'
        permissions = (
            ("can_read_dnspod_stat","查看dnspod_stat权限"),
            ("can_change_dnspod_stat", "更改dnspod_stat权限"),
            ("can_add_dnspod_stat", "添加dnspod_stat权限"),
            ("can_del_dnspod_stat", "删除dnspod_stat权限"),
        )









