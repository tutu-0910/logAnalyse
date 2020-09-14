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

class GitLogLoad(models.Model):
    git_log_url = models.CharField(max_length=100,verbose_name=u'gitClone路径', blank=True,db_index=True,default='')
    git_log_count = models.IntegerField(default=1, verbose_name=u'拉取的提交次数')
    git_log_time = models.DateTimeField(auto_now_add=True, verbose_name=u'最近一次拉取时间')

class GitLog(models.Model):
    hash = models.CharField(max_length=200,verbose_name=u'commitHash', blank=True, default='')
    auth = models.CharField(max_length=200,verbose_name=u'提交用户名', blank=True, default='')
    auth_email = models.CharField(max_length=200,verbose_name=u'提交用户密码', blank=True, default='',db_index=True)
    commit_at = models.DateTimeField(auto_now_add=False,db_index=True)
    add_line = models.IntegerField(default=1, verbose_name=u'用户增加行数')
    del_line = models.IntegerField(default=1, verbose_name=u'用户删除行数')
    company = models.CharField(max_length=200,verbose_name=u'用户公司', blank=True,db_index=True,default='')
    commit_file = models.CharField(max_length=200,verbose_name=u'用户提交路径', blank=True, default='')
    commit_path = models.CharField(max_length=200,verbose_name=u'用户提交大路径', blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)
    git_log_url = models.CharField(max_length=100,verbose_name=u'文件路径', blank=True,db_index=True,default='')