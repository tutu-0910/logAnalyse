# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import time
from django.shortcuts import render
from django.http import  HttpResponse
from . import settings 
import logging
import urllib2
from collections import Counter
from django.db import connection
from django.db import connection
import json
from collections import Counter
from django.http import JsonResponse
from copy import deepcopy
from django.http import HttpResponse
from django.shortcuts import render_to_response
import time
import datetime
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMessage
import requests
from django.db.models import Q
import time
import datetime
from . import models


import os
import subprocess
import calendar
import traceback
LOG = logging.getLogger(__name__)
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def addtodict2(thedict, key_a, key_b, val):
    if key_a in adic:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})


#git日志分析
@csrf_exempt
def setgitLogData(request):
    if request.method == "POST":
        #获取前端传递参数
        json_data = json.loads(request.body)
        print json_data
        author = json_data.get("author",'')
        startTime = json_data.get("startTime",'')
        endTime = json_data.get("endTime",'')
        gitCloneUrl = json_data.get("gitCloneUrl",'')
        gitpath = json_data.get("gitpath",'')
        commitFreq = json_data.get("commitFreq")
        email = json_data.get("email",'')
        file_type = json_data.get("file_type",'')
        #解析参数
        file_names = gitCloneUrl.split('/')
        #获取clone文件名
        file_name = "test"
        if file_names[len(file_names)-1]:
            file_name = file_names[len(file_names)-1]
        else:
            file_name = file_names[len(file_names)-2]
        #获取参数
        author_list = list(filter(None, author.split(';')))
        month_list = getBetweenMonth(startTime,endTime,commitFreq)
        gitpathList = list(filter(None, gitpath.split(';')))
        #查询数据入库
        gitLogAnalyze = models.GitLogAnalyze(
            git_clone_url = gitCloneUrl,
            git_path = gitpath,
            git_author = author,
            startTime=startTime,
            endTime=endTime,
            commit_freq=commitFreq,
            email = email
            )
        gitLogAnalyze.save()
        analyze_id = gitLogAnalyze.id
        #clone代码
        if os.path.isdir('/home/logAnalyse/gitlog/'+file_name):
            data1 = subprocess.Popen('cd /home/logAnalyse/gitlog/'+file_name+'; /home/logAnalyse/gitpull.sh', shell=True, stdout=subprocess.PIPE)
            data1.wait()
        else:
            data = subprocess.Popen('cd /home/logAnalyse/gitlog/; /home/logAnalyse/gitclone.sh '+ file_name+" "+ gitCloneUrl, shell=True, stdout=subprocess.PIPE)
            data.wait()
        print "....开始分析log..."
        if author=='' and gitpath=='':
            gitLogStatList = list()
            for i in range(0, len(month_list)-1, 1): 
                arg0 = month_list[i]+'-01'
                arg1 = month_list[i+1]+'-01'
                gitStat = subprocess.Popen('cd /home/logAnalyse/gitlog/'+file_name+'; /home/logAnalyse/gitLogStat_all.sh '+' ' + arg0 + ' ' +arg1,  shell=True, stdout=subprocess.PIPE)
                gitStat.wait()
                commit_count = gitStat.stdout.read()
                statData = models.GitLogPubStat(
                    end_time = arg1,
                    author = "all",
                    commit_count = commit_count,
                    commit_path = "all",
                    analyze_id = analyze_id
                )
                gitLogStatList.append(statData)
            models.GitLogPubStat.objects.bulk_create(gitLogStatList)
        elif author=='':
            gitLogStatList = list()
            for i in range(0, len(month_list)-1, 1): 
                for path in gitpathList:
                    arg0 = month_list[i]+'-01'
                    arg1 = month_list[i+1]+'-01'
                    gitStat = subprocess.Popen('cd /home/logAnalyse/gitlog/'+file_name+'; /home/logAnalyse/gitLogStat_path.sh '+' ' + arg0 + ' ' +arg1+ ' '+path,  shell=True, stdout=subprocess.PIPE)
                    gitStat.wait()
                    commit_count = gitStat.stdout.read()
                    statData = models.GitLogPubStat(
                        end_time = arg1,
                        author = "all",
                        commit_count = commit_count,
                        commit_path = path,
                        analyze_id = analyze_id
                    )
                    gitLogStatList.append(statData)
                print "分析log...."+month_list[i+1]
            models.GitLogPubStat.objects.bulk_create(gitLogStatList)
        elif gitpath=='':
            gitLogStatList = list()
            for i in range(0, len(month_list)-1, 1): 
                for author in author_list:
                    arg0 = month_list[i]+'-01'
                    arg1 = month_list[i+1]+'-01'
                    gitStat = subprocess.Popen('cd /home/logAnalyse/gitlog/'+file_name+'; /home/logAnalyse/gitLogStat_author.sh '+' '+author + ' ' + arg0 + ' ' +arg1,  shell=True, stdout=subprocess.PIPE)
                    gitStat.wait()
                    commit_count = gitStat.stdout.read()
                    statData = models.GitLogPubStat(
                        end_time = arg1,
                        author = author,
                        commit_count = commit_count,
                        commit_path = "all",
                        analyze_id = analyze_id
                    )
                    gitLogStatList.append(statData)
            models.GitLogPubStat.objects.bulk_create(gitLogStatList)
        else:     
            for i in range(0, len(month_list)-1, 1): 
                gitLogStatList = list()
                for author in author_list:
                    for path in gitpathList:
                        arg0 = month_list[i]+'-01'
                        arg1 = month_list[i+1]+'-01'
                        gitStat = subprocess.Popen('cd /home/logAnalyse/gitlog/'+file_name+'; /home/logAnalyse/gitLogStat.sh '+author + ' ' + arg0 + ' ' +arg1 + ' '+ path,  shell=True, stdout=subprocess.PIPE)
                        gitStat.wait()
                        commit_count = gitStat.stdout.read()
                        statData = models.GitLogPubStat(
                            end_time = arg1,
                            author = author,
                            commit_count = commit_count,
                            commit_path = path,
                            analyze_id = analyze_id
                        )
                        gitLogStatList.append(statData)
                models.GitLogPubStat.objects.bulk_create(gitLogStatList)
        print email 
        print file_type
        print type(file_type)
        output(analyze_id,file_name,email,file_type,gitLogAnalyze)
        response = HttpResponse(json.dumps({"code": 1}))
        response["Access-Control-Allow-Origin"] ="*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
    return response

#查询数据库并输出邮件发送给用户
def output(id,path,email,file_type,gitLogAnalyze):
    t = time.time()
    fileName=path+str(t)
    print id
    print fileName
    if file_type == 1:
        data = subprocess.Popen('cd /home/logAnalyse/gitlog/; /home/logAnalyse/gitsql.sh '+' ' + str(id) + " "+fileName,  shell=True, stdout=subprocess.PIPE)
        data.wait()
        file = fileName+".sql"
    else:
        sql = "select end_time,author,commit_count,commit_path from logAnalyse_gitlogpubstat where analyze_id="+str(id)
        data =  subprocess.Popen("cd /home/logAnalyse/gitlog/; /home/logAnalyse/gitexcel.sh "+" '" + sql + "' "+fileName,  shell=True, stdout=subprocess.PIPE)
        data.wait()
        file = fileName+".xls"
    #发送邮件给用户
    send_expired_email(file,email,gitLogAnalyze)
    return True


def send_expired_email(fileName, useremail,gitLogAnalyze):
    subject = (u'git提交记录查询结果')
  #  site_url = getattr(settings, "SITE_URL", "https://dw.pcl.ac.cn/cloud/")
  
    if gitLogAnalyze.git_path == '':
        gitLogAnalyze.git_path = 'all'
    if gitLogAnalyze.git_author == '':
        gitLogAnalyze.git_author = 'all'
    html_content = loader.render_to_string('send_gitlog_email.html',
                                           {"fileName": fileName,
                                           "gitHub_url":gitLogAnalyze.git_clone_url,
                                           "path":gitLogAnalyze.git_path,
                                           "auth":gitLogAnalyze.git_author,
                                           "freq":gitLogAnalyze.commit_freq,
                                           "startTime":gitLogAnalyze.startTime,
                                           "endtime":gitLogAnalyze.endTime})
    msg = EmailMessage(
        subject, html_content, settings.DEFAULT_FORM_EMAIL, [useremail])
    msg.content_subtype = "html"  # Main content is now html
    msg.send(fail_silently=False)
    return True


#获取华为各路径下的提交
def getHuaweiCommit(request):
    commitList = models.GitLogStat.objects.filter(id__gte=5011)
    gitLog_datas = list()
    for commit in commitList:
        data = dict(
            x = commit.end_time,
            y = commit.commit_count,
            s = commit.commit_path
        )
        gitLog_datas.append(data)
        print data
    return JsonResponse(gitLog_datas, safe=False)

def add_months(dt, months):
    # 返回dt隔months个月后的日期，months相当于步长

    month = dt.month - 1 + months
    year = int(dt.year + month / 12)
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def getBetweenMonth(begin_date, end_date, freq):
    # 返回所有月份，以及每月的起始日期、结束日期，字典格式
    date_list = list()
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m")
        date_list.append(date_str)
        begin_date = add_months(begin_date, freq)
    return date_list
        
