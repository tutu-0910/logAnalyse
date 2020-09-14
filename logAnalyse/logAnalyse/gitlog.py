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
from git import Repo
import pandas as pd

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
    print "发送邮件"
  
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

def send_gitlogJson_email(useremail,fileName):
    print "邮件发送"
    subject = (u'git提交记录查询结果')
    html_content = loader.render_to_string('send_json_email.html',
                                           {"fileName": fileName})
    msg = EmailMessage(
        subject, html_content, settings.DEFAULT_FORM_EMAIL, [useremail])
    msg.content_subtype = "html"  # Main content is now html
    msg.send(fail_silently=False)
    print "邮件发送成功"
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

#获取请求
@csrf_exempt
def getStat(request):
    gitLog_datas = list()
    if request.method == "POST":
        #获取前端传递参数
        json_data = json.loads(request.body)
        print json_data
        #通用参数
        anay_type = int( json_data.get("anay_type","0"))
        gitCloneUrl = json_data.get("gitCloneUrl",'')
        startTime = json_data.get("startTime",'')
        endTime = json_data.get("endTime",'')
        email = json_data.get("email",'')
        #anay_type = 1
        gitpath = json_data.get("gitpath",'')
        author = json_data.get("author",'')
        freq = json_data.get("commitFreq")
        file_type = json_data.get("file_type")
        #anay_type = 2
        file_path = json_data.get("file_path")
        #anay_type = 3
        company = json_data.get("company")
        company_file_path = json_data.get("company_path")
        #anay_type = 4
        freq_company = json_data.get("freq_company")
        freq_path = json_data.get("freq_path")
        #解析参数
        file_names = gitCloneUrl.split('/')
        #获取clone文件名
        file_name = "test"
        if file_names[len(file_names)-1]:
            file_name = file_names[len(file_names)-1]
        else:
            file_name = file_names[len(file_names)-2]
        #判断该目录文件是否被clone到本地
        if os.path.isdir('/home/logAnalyse/gitlog/'+file_name):
            data1 = subprocess.Popen('cd /home/logAnalyse/gitlog/'+file_name+'; /home/logAnalyse/gitpull.sh', shell=True, stdout=subprocess.PIPE)
            data1.wait()
        else:
            data = subprocess.Popen('cd /home/logAnalyse/gitlog/; /home/logAnalyse/gitclone.sh '+ file_name+" "+ gitCloneUrl, shell=True, stdout=subprocess.PIPE)
            data.wait()
        #初始化日志数据
        loadGitlog(file_name)
        print "....开始分析log..."
        if anay_type ==  1:
            getAllStat(gitCloneUrl,file_name,gitpath,author,startTime,endTime,freq,email,file_type)
        else:
            if anay_type == 2:
                #以公司为单位统计(以同一邮箱后缀为一个公司),不同公司的代码贡献量
                gitLog_datas = getAllAuthor(file_name,file_path,startTime,endTime)
            elif anay_type == 3:
                #指定公司在某个目录下的提交情况
                gitLog_datas = getPathStat(file_name,company_file_path,company,startTime,endTime)
            elif anay_type == 4:
                gitLog_datas = getTimeStat(file_name,freq_path,freq_company,startTime,endTime,freq)
            #将gitlog写入文件
            t = time.time()
            fileName=file_name+str(t)+".txt"
            f2 = open('/home/logAnalyse/logAnalyse/gitlogStatic/logfile/'+fileName,'w')
            f2.write(str(gitLog_datas))
            f2.close()
            #gitdatas发送至邮箱
            send_gitlogJson_email(email,fileName)
        response = HttpResponse(json.dumps({"code": 1}))
        response["Access-Control-Allow-Origin"] ="*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
    return response
      

#初始化log数据        
def loadGitlog(file_name):
    #获取gitLog信息
    r = Repo('/home/logAnalyse/gitlog/'+file_name)
    #获取该路径下上次拉取的时间
    try:
        last_time = models.GitLogLoad.objects.values("git_log_time").filter(git_log_url=file_name).order_by('-git_log_time')[:1]
        if last_time:
            last_time = ""
        else:
            last_time = "2000-01-01"
    except:
        last_time = "2000-01-01"
    #获取gitLog最新commit总数
    arg0 = last_time
    gitStat = subprocess.Popen('cd /home/logAnalyse/gitlog/'+file_name+'; /home/logAnalyse/gitCount.sh '+arg0,  shell=True, stdout=subprocess.PIPE)
    gitStat.wait()
    commit_count = gitStat.stdout.read()
    #分析gitlog日志
    for j in range(450000, int(commit_count), 1000):
        print j
        skip = "--skip="+str(j)
        log = r.git.log('--pretty=format:|%H|%h|%ae|%an|%ce|%cn|%at|%ad|', "--numstat", "--after='"+last_time+"'", "-n 1000",skip)
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
                    add_line = commitFile[0]
                    del_line = commitFile[1]
                    try:
                        add_line = int(add_line)
                        del_line = int(del_line)
                        gitlog = models.GitLog(
                            hash = hash,
                            auth = auth,
                            auth_email = auth_email,
                            commit_at = t ,
                            add_line = add_line,
                            del_line = del_line,
                            commit_file = commit_file,
                            company = company,
                            git_log_url = file_name
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
        try:
            models.GitLog.objects.bulk_create(gitlogList)
        except Exception as e:
            LOG.info("Unknown Error %s", e)
    #更新拉去时间
    gitlogLoad = models.GitLogLoad(
                            git_log_count = int(commit_count),
                            git_log_url = file_name
                        )
    gitlogLoad.save()


#只获取统计结果
def getAllStat(gitCloneUrl,file_name,gitpath,author,startTime,endTime,freq,email,file_type):
     #获取参数
        author_list = list(filter(None, author.split(';')))
        month_list = getBetweenMonth(startTime,endTime,freq)
        gitpathList = list(filter(None, gitpath.split(';')))
        #查询数据入库
        gitLogAnalyze = models.GitLogAnalyze(
            git_clone_url = gitCloneUrl,
            git_path = gitpath,
            git_author = author,
            startTime=startTime,
            endTime=endTime,
            commit_freq=freq,
            email = email
            )
        gitLogAnalyze.save()
        analyze_id = gitLogAnalyze.id
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
        output(analyze_id,file_name,email,file_type,gitLogAnalyze)
#以公司为单位统计(以同一邮箱后缀为一个公司),不同公司的代码贡献量
def getAllAuthor(file_name,gitpath,startTime,endTime):
    #初始化日志
    loadGitlog(file_name)
    #根据需求统计结果
    gitLog_datas = list()
    #全路径统计
    if gitpath=='':
        sql = "select count(*) as count,company from (select * from logAnalyse_gitlog where commit_at between '"+startTime+"' and '"+endTime+"' GROUP BY `hash` ORDER BY id desc) a GROUP BY company ORDER BY count desc;"
    else:#指定路径统计
        sql = "select count(*) as count,company from (select * from logAnalyse_gitlog where git_log_url = '"+file_name+"' commit_at between '"+startTime+"' and '"+endTime+"' and  commit_file like '"+gitpath+"%' GROUP BY `hash` ORDER BY id desc) a GROUP BY company ORDER BY count desc;"
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        data = dict(
            company = result[1],
            count = result[0]
        )
        gitLog_datas.append(data)
    return gitLog_datas


#某个单位提交者不同目录下的提交情况统计
def getPathStat(file_name,file_path,company,startTime,endTime):
    gitLog_datas = list()
    #paths = ["drivers","fs","tools","arch","net","include","sound","kernel"]
    if file_path == '':
        file_path = "/home/logAnalyse/gitlog/"+file_name
    else:
        file_path = "/home/logAnalyse/gitlog/"+file_name+"/"+file_path
    pathList = getDirList(file_path)
    #paths = ["drivers/net/","drivers/scsi/","drivers/infiniband/","drivers/gpu/","drivers/staging/","drivers/crypto/","drivers/usb/","drivers/iio/","drivers/pci/","drivers/spi/","drivers/irqchip/"]
    for path in pathList:
        sql = "select count(*) as count from (select * from logAnalyse_gitlog where commit_at between '"+startTime+"' and '"+endTime+"' and company in ('"+company+"') and  commit_file like '"+path+"%' GROUP BY `hash` ORDER BY id desc) a order by count desc;"
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            data = dict(
                path = path,
                count = result[0]
            )
            gitLog_datas.append(data)
    return gitLog_datas

#获取指定公司指定文件夹下的按时间分布的提交情况
def getTimeStat(file_name,path,company,startTime,endTime,freq):
    gitLog_datas = list()
    month_list = getBetweenMonth(startTime, endTime,freq)
    for i in range(0, len(month_list)-1, 1):
        startTime = month_list[i]+"-01"
        endTime = month_list[i+1]+"-01"
        #drivers/net/ethernet/hisilicon
        #sql = "select count(*) from (select * from khatch_api_gitlog where commit_at BETWEEN '"+startTime+"' and '"+endTime +"' and company in ('huawei','hisilicon.com') and  commit_file like 'drivers/net/ethernet/hisilicon%' GROUP BY `hash`) a;"
        sql = "select count(*) from (select * from logAnalyse_gitlog where commit_at BETWEEN '"+startTime+"' and '"+endTime +"' and company in ('"+company+"') and  commit_file like '"+path+"%' GROUP BY `hash`) a;"
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            data = dict(
                time = endTime,
                count = result[0]
            )
            gitLog_datas.append(data)
    return gitLog_datas


#获取指定目录下的文件夹
def getDirList(path):
    dbtype_list = os.listdir(path)
    for dbtype in dbtype_list:
        if os.path.isfile(os.path.join(path,dbtype)):
            dbtype_list.remove(dbtype)
    return dbtype_list