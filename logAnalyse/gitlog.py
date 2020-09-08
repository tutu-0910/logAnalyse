# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
import time
from django.shortcuts import render
from django.http import  HttpResponse
from khatch import settings as khatch_settings
import logging
import urllib2
from collections import Counter
from django.db import connection
from django.db import connection
import json
from collections import Counter
from django.http import JsonResponse
from copy import deepcopy
from khatch_api import models
from khatch_api.api import utils as rest_utils
from django.http import HttpResponse
from django.shortcuts import render_to_response
import time
import datetime
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMessage
import hashlib
import base64
from hashlib import sha256
import requests
from django.db.models import Q
import time
import datetime

import os
import subprocess
import calendar
from git import Repo
import pandas as pd
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
        file_type = json_data.get("type",'')
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
        if os.path.isdir('/home/gitlog/'+file_name):
            data1 = subprocess.Popen('cd /home/gitlog/'+file_name+'; /home/gitlog/gitpull.sh', shell=True, stdout=subprocess.PIPE)
            data1.wait()
        else:
            data = subprocess.Popen('cd /home/gitlog; /home/gitlog/gitclone.sh '+ file_name+" "+ gitCloneUrl, shell=True, stdout=subprocess.PIPE)
            data.wait()
        print "....开始分析log..."
        if author=='' and gitpath=='':
            gitLogStatList = list()
            for i in range(0, len(month_list)-1, 1): 
                arg0 = month_list[i]+'-01'
                arg1 = month_list[i+1]+'-01'
                gitStat = subprocess.Popen('cd /home/gitlog/'+file_name+'; /home/gitlog/gitLogStat_all.sh '+' ' + arg0 + ' ' +arg1,  shell=True, stdout=subprocess.PIPE)
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
                    gitStat = subprocess.Popen('cd /home/gitlog/'+file_name+'; /home/gitlog/gitLogStat_path.sh '+' ' + arg0 + ' ' +arg1+ ' '+path,  shell=True, stdout=subprocess.PIPE)
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
                    gitStat = subprocess.Popen('cd /home/gitlog/'+file_name+'; /home/gitlog/gitLogStat_author.sh '+' '+author + ' ' + arg0 + ' ' +arg1,  shell=True, stdout=subprocess.PIPE)
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
                        gitStat = subprocess.Popen('cd /home/gitlog/'+file_name+'; /home/gitlog/gitLogStat.sh '+author + ' ' + arg0 + ' ' +arg1 + ' '+ path,  shell=True, stdout=subprocess.PIPE)
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
        output(analyze_id,file_name,email,file_type)
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
    if file_type == 'sql':
        data = subprocess.Popen('cd /home/gitlog/; /home/gitlog/gitsql.sh '+' ' + str(id) + ' ' +path+" "+fileName,  shell=True, stdout=subprocess.PIPE)
        data.wait()
        file = fileName+".sql"
    else:
        sql = "select end_time,author,commit_count,commit_path from khatch_api_gitlogpubstat where analyze_id="+str(id)
        data =  subprocess.Popen("cd /home/gitlog/; /home/gitlog/gitexcel.sh "+" '" + sql + "' " +path+" "+fileName,  shell=True, stdout=subprocess.PIPE)
        data.wait()
        file = fileName+".xsl"
    #发送邮件给用户
    send_expired_email(file,email,gitLogAnalyze)
    return True


def send_expired_email(fileName, useremail,gitLogAnalyze):
    subject = (u'git提交记录查询结果')
    site_url = getattr(settings, "SITE_URL", "https://dw.pcl.ac.cn/cloud/")
    html_content = loader.render_to_string('send_gitlog_email.html',
                                           {"fileName": fileName,
                                           "gitHub_url":gitLogAnalyze.git_clone_url,
                                           "path":gitLogAnalyze.gitpath,
                                           "auth":gitLogAnalyze.author,
                                           "freq":gitLogAnalyze.commitFreq,
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
        

def setlinaroGitStat(request):
    author = '@linaro.org';
    startTime = '2010-01-01';
    endTime = '2020-09-01';
    month_list = getBetweenMonth(startTime, endTime,6)
    pathList = ['drivers/','tools/']
    for i in range(0, len(month_list)-1, 1):
        for path in pathList:
            print path + "..."+ month_list[i]+'-01'
            gitLogStatList = list()
            arg0 = month_list[i]+'-01'
            arg1 = month_list[i+1]+'-01'
            arg2 = path
            #data = subprocess.Popen('cd /home/linux/linux/; /home/linux/groupHuawei.sh '+ arg0+" "+ arg1,shell=True, stdout=subprocess.PIPE)
            data = subprocess.Popen('cd /home/linux/linux; /home/linux/groupLinaro.sh '+ arg0+" "+ arg1+" "+arg2,shell=True, stdout=subprocess.PIPE)
            data.wait()
            commit_count = data.stdout.read()
            print commit_count
            statData = models.GitLogStat(
                end_time =  arg1,
                company = author,
                commit_path = path,
                commit_count = int(commit_count)
            )
            gitLogStatList.append(statData)
            data1 = subprocess.Popen('cd /home/linux/linux; /home/linux/groupAll.sh '+ arg0+" "+ arg1+" "+arg2,shell=True, stdout=subprocess.PIPE)
            data1.wait()
            commit_count1 = data1.stdout.read()
            print commit_count1
            statData1 = models.GitLogStat(
                end_time =  arg1,
                company = 'all',
                commit_path = path,
                commit_count = int(commit_count1)
            )
            gitLogStatList.append(statData1)
            models.GitLogStat.objects.bulk_create(gitLogStatList)

    return JsonResponse("data", safe=False)

def setHuagitlog(request):
    r = Repo('/home/gitlog/linux')
    emailList = ['phytium.com.cn', 'kylinos.cn', 'huawei.com','ubuntukylin.com','kylinos.cn']
    for j in range(0, 950000, 1000):
        print j
        skip = "--skip="+str(j)
        log = r.git.log('--pretty=format:|%H|%h|%ae|%an|%ce|%cn|%at|%ad|', "--numstat", "--after='2020-08-05'", "-n 1000",
                        skip)
        # 用'|'分割返回的字符串
        msg = log.split('|')
        # 忽略首个空白的字符串
        msg = msg[1:]
        # 计算有多少个返回的日志与消息
        ver_num = int(len(msg) / 9)
        # 文件列表的偏移量是 8,如果改动前面的--pretty参数，请重新计算偏移量
        offset = 8
        # 遍历每个提交的偏移量
        gitlogList = []
        for i in range(ver_num):
            # 获取每个修改的文件列表
            auth_email = msg[2 + i*9]
            email = ''
            try:
                email = auth_email.split('@')[1]
            except Exception:
                print auth_email.split('@')

            #if email in emailList:
            if True:
                company = ''
                if auth_email.endswith('phytium.com.cn'):
                    company = 'phytium'
                elif auth_email.endswith('huawei.com'):
                    company = 'huawei'
                elif auth_email.find('kylin') != -1:
                    company = 'kylin'
                else:
                    company = email
                hash = msg[i * 9]
                auth = msg[3 + i * 9]
                t = int(msg[6 + i * 9])
                t = datetime.date.fromtimestamp(t)
                file_list = msg[offset + i * 9]
                # 分割提取每一个项目，拟用\t字符去分割
                file_list = file_list.replace('\n', '\t')
                info = file_list.split('\t')
                # 去除空行
                info = [i for i in info if len(i.strip()) > 0]
                step = 3
                infoArray = [info[i:i + step] for i in range(0, len(info), step)]
                for commitFile in infoArray:
                    if len(commitFile) > 0:
                        commit_file = commitFile[2]
                        #if commit_file.startswith('arch/arm64'):
                        if True:
                            add_line = commitFile[0]
                            del_line = commitFile[1]
                            try:
                                add_line = int(add_line)
                                del_line = int(del_line)
                                print hash
                                gitlog = models.GitLog(
                                    hash = hash,
                                    auth = auth,
                                    auth_email = auth_email,
                                    commit_at = t ,
                                    add_line = add_line,
                                    del_line = del_line,
                                    commit_file = commit_file,
                                    company = company
                                )
                                gitlogList.append(gitlog)
                            except Exception as e:
                                LOG.info("Unknown Error %s", e)
                # 有些提交的info是空，没有任何文本的修改，比如说，只修改了文件的属性，提交了版本库，无实质性的修改。
                # 所以info可能为空，啥都没有。
                # 如果有内容，其内容是：
                # 修改增加行数	修改删除行数	文件名(全路径)
                # . . .
                # 将unix时间转换为标准日期时间(0时区)
                #t = int(msg[6 + i * 9])
                #t = datetime.date.fromtimestamp(t)
        try:
            models.GitLog.objects.bulk_create(gitlogList)
        except Exception as e:
            LOG.info("Unknown Error %s", e)
    return JsonResponse("data", safe=False)


def getAllPath(request):
    gitLog_datas = list()
    #全路径统计
    #sql = "select count(*) as count,company from (select * from khatch_api_gitlog where commit_at > '2015-01-01' GROUP BY `hash` ORDER BY id desc) a GROUP BY company ORDER BY count desc limit 0,30;"
    #arm路径统计
    sql="select count(*) as count,company from (select * from khatch_api_gitlog where commit_at > '2015-01-01' and  commit_file like 'arch/arm64%' GROUP BY `hash` ORDER BY id desc) a GROUP BY company ORDER BY count desc;"
    print sql
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        data = dict(
            y = result[0],
            x = result[1],
            s = 1
        )
        gitLog_datas.append(data)
    return JsonResponse(gitLog_datas, safe=False)
def getPathStat(request):
    gitLog_datas = list()
    #paths = ["drivers","fs","tools","arch","net","include","sound","kernel"]
    paths = ["drivers/net/","drivers/scsi/","drivers/infiniband/","drivers/gpu/","drivers/staging/","drivers/crypto/","drivers/usb/","drivers/iio/","drivers/pci/","drivers/spi/","drivers/irqchip/"]
    for path in paths:
        sql = "select count(*) as count from (select * from khatch_api_gitlog where commit_at > '2015-01-01' and company in ('huawei','hisilicon.com') and  commit_file like '"+path+"%' GROUP BY `hash` ORDER BY id desc) a ;"
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            data = dict(
                y = result[0],
                x = path,
                s = 1
            )
            gitLog_datas.append(data)
    return JsonResponse(gitLog_datas, safe=False)

def getTimeStat(request):
    gitLog_datas = list()
    month_list = getBetweenMonth("2016-04-01", "2020-09-01",3)
    for i in range(0, len(month_list)-1, 1):
        startTime = month_list[i]+"-01"
        endTime = month_list[i+1]+"-01"
        #drivers/net/ethernet/hisilicon
        #sql = "select count(*) from (select * from khatch_api_gitlog where commit_at BETWEEN '"+startTime+"' and '"+endTime +"' and company in ('huawei','hisilicon.com') and  commit_file like 'drivers/net/ethernet/hisilicon%' GROUP BY `hash`) a;"
        sql = "select count(*) from (select * from khatch_api_gitlog where commit_at BETWEEN '"+startTime+"' and '"+endTime +"' and company in ('huawei','hisilicon.com') and  commit_file like 'drivers/infiniband/hw/hn%' GROUP BY `hash`) a;"
        print sql
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            data = dict(
                y = result[0],
                x = endTime,
                s = 1
            )
            gitLog_datas.append(data)
    return JsonResponse(gitLog_datas, safe=False)
