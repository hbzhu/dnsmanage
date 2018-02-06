# -*- coding: utf-8 -*-
"""
__author__ = 'Frank'
__mtime__ = '2017/12/22'
"""
from django.contrib import admin
from . import models

admin.site.register(models.Dnspod_domains)
admin.site.register(models.Dnspod_records)

