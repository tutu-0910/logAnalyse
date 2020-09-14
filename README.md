
![](https://github.com/tutu-0910/logAnalyse/blob/master/logAnalyse/gitlogStatic/img/favicon.ico)<br>

### 开发单位：鹏城实验室(PCL)


- [ 开源软件代码贡献排名统计平台v1.0 ](#head1)
	- [ 平台介绍](#head2)
	- [ 平台运行说明](#head3)
		- [ 一、环境配置、安装要求](#head5)
		- [ 二、输入参数规范](#head10)
		- [ 三、输出结果说明](#head14)
	- [ 访问地址](#head18)
	- [ 分析结果展示示例](#head19)



# <span id="head1">开源软件代码贡献排名统计平台v1.0</span>

## <span id="head2"> 平台介绍</span>

开源软件代码贡献排名统计平台旨在分析重要开源软件栈不同开发者的贡献情况，尤其是大中华区团队开发者的贡献（TODO）。

1. 分析不同开发者的开源软件代码的贡献量；
2. 分析开发者在开源软件代码的不同目录下的共享量；
3. 分析开发者在不同时间段对不同目录下代码的贡献量；
4. 分析结果形成柱状图和曲线图（TODO）

统计平台脚本组成如下：

1. 分析gitLog日志的脚本文件(*.sh)
2. 分析gitLog日志的脚本文件(*.sh)
3. 输入需要分析的参数，并输出处理结果的django工程代码(logAnalyse/)
	


***NOTE：后续文档的主要内容为代码环境配置、安装要求，输入参数规范，输出结果说明等组成***

## <span id="head3"> logAnalyse运行说明</span>

### <span id="head4"> 本文用于在CentOS环境下运行</span>

### <span id="head5"> 一、环境配置、安装要求</span>


#### 环境要求

项 | 要求
---|---
节点配置 | 不少于2核4GB
操作系统 | Linux（本文档基于Centos7）
Python | 2.7
Django | 1.10
mysql  | 5.6.45


#### 安装步骤
*创建目录*

```
cd home
mkdir logAnalyse
cd logAnalyse
```

*下载代码*

```
git clone https://github.com/tutu-0910/logAnalyse.git
```

*修改配置文件*

```
vi logAnalyse/logAnalyse/settings.py
```

*修改以下内容*

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gitlog',
        'USER': 'root',
        'PASSWORD': '123123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}
用户名和密码修改为自己数据库的用户名和密码

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST = 'smtp.xxx.xxx.xxx'
EMAIL_HOST_USER = 'username@xxx.xxx.xxx'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FORM_EMAIL = 'username<usename@xxx.xxx.xxx>'

邮件服务器修改问自己的邮件服务器

```

*初始化数据库*

```
cd /home/logAnalyse/logAnalyse
python manage.py makemigrations
python manage.py migrate
```

*启动服务*

```
python manage.py runserver 0.0.0.0:8000
```
*访问服务*
```
ip:8000
```
### <span id="head10"> 二、输入参数规范</span>

统计平台脚本组成如下：

1. 输入正确gitHub clone地址；
2. 输入需要统计的文件或文件夹的路径，用英文;隔开(如果统计所有路径总提交情况，则可不输入)；
3. 输入需要统计的提交者用户名或邮箱地址(支持模糊匹配)，用英文;隔开(如果统计所有用户总提交情况，则可不输入)；
4. 选择统计的提交频率；；
5. 选择需要统计的开始时间和结束时间；
6. 选择接受数据的方式，可以是sql表结构+数据，也可以是excel形式；
7. 输入正确的接收数据的邮箱。

### <span id="head14"> 三、输出结果说明</span>

统计结果会以邮件形式发送至填写的接收邮箱，请注意查收邮件。


## <span id="head18">访问地址</span>
https://dw.pcl.ac.cn/gitlog/
## <span id="head19">分析结果展示示例</span>
https://dw.pcl.ac.cn/dwmain/gitLogStat.html
1.选择时间
