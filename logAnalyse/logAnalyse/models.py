# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime
import uuid

class GitLogPubStat(models.Model):
    end_time = models.CharField(max_length=10,verbose_name=u'提交时间', blank=True,db_index=True,default='')
    author = models.CharField(max_length=50,verbose_name=u'用户名', blank=True,db_index=True,default='')
    commit_count = models.IntegerField(default=1, verbose_name=u'提交次数')
    commit_path =  models.CharField(max_length=50,verbose_name=u'提交路径', blank=True,db_index=True,default='')
    analyze_id = models.IntegerField(default=1, verbose_name=u'查询id')

class GitLogAnalyze(models.Model):
    git_clone_url = models.CharField(max_length=100,verbose_name=u'gitClone路径', blank=True,db_index=True,default='')
    git_path = models.CharField(max_length=500,verbose_name=u'代码路径', blank=True,default='')
    git_author = models.CharField(max_length=500,verbose_name=u'代码提交者', blank=True,default='')
    startTime = models.CharField(max_length=50,verbose_name=u'开始时间', blank=True,default='')
    endTime = models.CharField(max_length=50,verbose_name=u'结束时间', blank=True,default='')
    commit_freq = models.CharField(max_length=3,verbose_name=u'统计提交频率', blank=True,default='')
    email = models.CharField(max_length=50,verbose_name=u'接收数据的邮箱', blank=True,db_index=True,default='')
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    