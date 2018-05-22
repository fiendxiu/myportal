from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


CACTI = (
    (u'cacti1',u'cacti1'),
    (u'cacti2',u'cacti2'),
    (u'cacti3',u'cacti3'),
)
NETFLOW = (
    (u'netflow1',u'netflow1'),
    (u'netflow2',u'netflow2'),
    (u'netflow3',u'netflow3'),
)

# Create your models here.

class Customer(models.Model):
    username = models.CharField(u'用户名', max_length=40)
    contract = models.CharField(u'合同名', max_length=100)
    sale = models.CharField(u'客户经理', max_length=100)
    email = models.EmailField(u'客户经理邮箱')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.username, self.contract)

class Cacti(models.Model):
    username = models.CharField(u'用户名', max_length=40)
    description = models.CharField(u'描述', max_length=100)
    server = models.CharField(u'服务器', max_length=10, choices=CACTI,default=u'cacti1')
    graphid = models.CharField(u'图形ID', max_length=10, default='0')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s ' % (self.username, self.description)

def reporturl_handler(instance,filename):
    return "static/report/{user}/{file}".format(user=instance.username,file=filename)

class Report(models.Model):
    username = models.CharField(u'用户名', max_length=40)
    filename = models.CharField(max_length=255,blank=True)
    fileurl = models.FileField(upload_to=reporturl_handler)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    def __str__(self):
        return self.filename

class Availability(models.Model):
    username = models.CharField(u'用户名', max_length=40)
    ip = models.CharField(u'IP', max_length=20)
    description = models.CharField(u'描述', max_length=100)
    triggerid = models.CharField(u'触发器ID', max_length=10)
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s --- %s' % (self.username, self.ip, self.description)

class Netflow(models.Model):
    username = models.CharField(u'用户名', max_length=40)
    j_username = models.CharField(u'Netflow帐号', max_length=40)
    j_password = models.CharField(u'Netflow密码', max_length=40)
    server = models.CharField(u'服务器', max_length=10, choices=NETFLOW,default=u'netflow1')
    create_date = models.DateTimeField(u'创建日期',default=timezone.now)
    mod_date = models.DateTimeField(u'最后修改日期', auto_now = True)
    def __str__(self):
        return  u'%s --- %s' % (self.username, self.j_username)
