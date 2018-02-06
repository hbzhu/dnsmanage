# -*- coding: utf-8 -*-
"""
__author__ = 'Frank'
__mtime__ = '2018/1/25'
"""
from django.contrib import admin
from . import models

admin.site.register(models.User)
#admin.site.register(models.UserGroup)
#admin.site.register(models.AdminGroup)
#admin.site.register(models.Permission)