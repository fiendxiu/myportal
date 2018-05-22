from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from portal.models import *
from django.db import IntegrityError
from django.db.models import Q

from portal.form import *
import urllib.request,os,datetime

# Create your views here.

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')
        else:
            return render(request,'page-login.html',{'error':'错误的 用户名/密码'})
    if 'resetpw' in request.GET:
        return render(request,'page-login.html',{'error':'已重置密码，请重新登入'})
    return render(request,'page-login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def paging(data,page):
    '''
    @todo:将数据列表对象分页，并返回第n页的列表。
    Paginator(data,X)第二个参数X控制每页列表包含几条数据
    '''
    paginator = Paginator(data,8)
    try:
        newpage=int(page)
    except ValueError:
        newpage=1
    try:
        room = paginator.page(newpage)
    except PageNotAnInteger:
        room = paginator.page(1)
    except EmptyPage:
        room = paginator.page(paginator.num_pages)
    return room

@csrf_exempt
def index(request):
    '''
    @todo:客户帐号认证后显示客户页(index)，管理员帐号认证后显示管理页(administrator)
    管理页：~Q表示不等于，即隐藏管理员帐号，避免被错误修改或删除
    客户页：get空数据会触发异常，filter则不会，so get放try里。首页显示简单信息
    '''
    if request.user.is_authenticated:
        if request.user.has_perm('auth.change_group'):
            customers = User.objects.filter(~Q(username='admin')).order_by('-id')
            room = paging(customers,request.GET.get('page','1'))
            return render(request,'administrator.html',{'room':room})
        else:
            try:
                customer = Customer.objects.get(username=request.user.username)
            except:
                customer = False
            cacti = Cacti.objects.filter(username=request.user.username)
            availability = Availability.objects.filter(username=request.user.username)
            nflow = Netflow.objects.filter(username=request.user.username)
            report = Report.objects.filter(username=request.user.username)
            return render(request,'index.html',{'customer':customer,'cacti':len(cacti),'availability':len(availability),'nflow':nflow,'report':len(report)})
    return HttpResponseRedirect('/login/')

def search(request):
    '''
    @todo:搜索客户，需要管理员权限
    '''
    if request.user.is_authenticated:
        if request.user.has_perm('auth.change_group'):
            if 'username' in request.GET:
                q = request.GET['username']
                data = User.objects.filter(~Q(username='admin'),username__icontains=q)
                room = paging(data,request.GET.get('page','1'))
                if room:
                    return render(request,'administrator.html',{'room':room})
                else:
                    return render(request,'administrator.html',{'room':room,'error':'没有匹配的结果'})
            return HttpResponseRedirect('/')
        return render(request,'page-error-404.html')
    return HttpResponseRedirect('/login/')

def account(request,username):
    '''
    @todo:单个用户信息的管理页，需要管理员权限
    '''
    if request.user.is_authenticated:
        if request.user.has_perm('auth.change_group'):
            report = Report.objects.filter(username=username)
            form = Reportform
            if request.method == "POST":
                reportform = Reportform(request.POST, request.FILES)
                if reportform.is_valid():
                    report = Report()
                    report.username = reportform.cleaned_data["username"]
                    report.filename = reportform.cleaned_data["fileurl"].name
                    report.fileurl = reportform.cleaned_data["fileurl"]
                    report.save()
                return HttpResponseRedirect('/account/'+username)
            account = User.objects.get(username=username)
            customer = Customer.objects.filter(username=username)
            netflow = Netflow.objects.filter(username=username)
            cacti = Cacti.objects.filter(username=username)
            availability = Availability.objects.filter(username=username)
            return render(request,'account.html',{'account':account,'customer':customer,'netflow':netflow,'cacti':cacti,'availability':availability,'report':report,'form':form,'username':username})
        return render(request,'page-error-404.html')
    return render(request,'page-login.html')

@csrf_exempt
def reset_passwd(request,username):
    '''
    @todo:重置密码
    空密码触发异常，刷新页面并提示
    修改自己帐号的密码，重定向到登入页并提示
    管理员能够修改其他帐号密码，非管理员不能
    '''
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                if not request.POST['password']:
                    raise UserWarning
                if request.user.username == username:
                    user = User.objects.get(username=username)
                    user.set_password(request.POST['password'])
                    user.save()
                    return HttpResponseRedirect('/login/?resetpw')
                else:
                    if request.user.has_perm('auth.change_group'):
                        user = User.objects.get(username=username)
                        user.set_password(request.POST['password'])
                        user.save()
                        return render(request,'resetpasswd.html',{'error':'已重置密码'})
                    else:
                        return render(request,'resetpasswd.html',{'error':'无权限 尝试修改非本账户的密码'})
            except UserWarning:
                return render(request,'resetpasswd.html',{'error':'密码 不能为空'})
        return render(request,'resetpasswd.html')
    return render(request,'page-login.html')

@csrf_exempt
def isActive(request,username):
    '''
    @todo:切换账号的激活状态，需要管理员权限
    '''
    if request.user.is_authenticated:
        if request.user.has_perm('auth.change_group'):
            user = User.objects.get(username=username)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            return HttpResponseRedirect('/account/'+username)
        return render(request,'page-error-404.html')
    return render(request,'page-login.html')

@csrf_exempt
def delete(request,key,username):
    '''
    @todo:删除key对象的操作，需要管理员权限
    '''
    if request.user.is_authenticated:
        if request.user.has_perm('auth.change_group'):
            if key == 'user':
                user = User.objects.get(username=username)
                user.delete()
                return HttpResponseRedirect('/')
            elif key == 'customer':
                customer = Customer.objects.get(id=username)
                customer.delete()
                return HttpResponseRedirect('/account/'+customer.username)
            elif key == 'netflow':
                netflow = Netflow.objects.get(id=username)
                netflow.delete()
                return HttpResponseRedirect('/account/'+netflow.username)
            elif key == 'cacti':
                cacti = Cacti.objects.get(id=username)
                cacti.delete()
                return HttpResponseRedirect('/account/'+cacti.username)
            elif key == 'availability':
                availability = Availability.objects.get(id=username)
                availability.delete()
                return HttpResponseRedirect('/account/'+availability.username)
            elif key == 'report':
                report = Report.objects.get(id=username)
                report.delete()
                fileurl = report.fileurl
                os.remove(str(fileurl))
                return HttpResponseRedirect('/account/'+report.username)
            return render(request,'page-error-404.html')
        return render(request,'page-error-404.html')
    return render(request,'page-login.html')

def edit(request,key,username):
    '''
    @todo:编辑key对象的操作，需要管理员权限
    '''
    if request.user.is_authenticated:
        if request.user.has_perm('auth.change_group'):
            if key == 'customer':
                editModel = get_object_or_404(Customer,pk=username)
                if request.method == 'POST':
                    form = Customerform(request.POST,instance=editModel)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+editModel.username)
                form = Customerform(instance=editModel)
                return render(request,'editcustomer.html',{'form':form})
            elif key == 'netflow':
                editModel = get_object_or_404(Netflow,pk=username)
                if request.method == 'POST':
                    form = Netflowform(request.POST,instance=editModel)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+editModel.username)
                form = Netflowform(instance=editModel)
                return render(request,'editnetflow.html',{'form':form})
            elif key == 'cacti':
                editModel = get_object_or_404(Cacti,pk=username)
                if request.method == 'POST':
                    form = Cactiform(request.POST,instance=editModel)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+editModel.username)
                form = Cactiform(instance=editModel)
                return render(request,'editcacti.html',{'form':form})
            elif key == 'availability':
                editModel = get_object_or_404(Availability,pk=username)
                if request.method == 'POST':
                    form = Availabilityform(request.POST,instance=editModel)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+editModel.username)
                form = Availabilityform(instance=editModel)
                return render(request,'editavailability.html',{'form':form})
        return render(request,'page-error-404.html')
    return render(request,'page-login.html')

def add(request,key,username):
    '''
    @todo:增加key对象的操作，需要管理员权限
    '''
    if request.user.is_authenticated:
        if request.user.has_perm('auth.change_group'):
            if key == 'user':
                if request.method == 'POST':
                    try:
                        if not request.POST['password'] or not request.POST['username']:
                            raise UserWarning
                        user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
                        user.is_active = True
                        user.save()
                    except IntegrityError:
                        return render(request,'adduser.html',{'error':'用户名 已存在'})
                    except UserWarning:
                        return render(request,'adduser.html',{'error':'用户名/密码 不能为空'})
                    except:
                        return render(request,'adduser.html',{'error':'提交的数据可能存在异常，账户无法创建'})
                    else:
                        return HttpResponseRedirect('/')
                return render(request,'adduser.html')
            if key == 'customer':
                if request.method == 'POST':
                    request.POST=request.POST.copy()
                    form = Customerform(request.POST)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+username)
                    else:
                        return render(request,'addcustomer.html',{'error':'提交的数据可能存在异常，客户信息无法创建'})
                form = Customerform(auto_id=False)
                form.fields['username'].initial = username
                return render(request,'addcustomer.html',{'form':form})
            if key == 'netflow':
                if request.method == 'POST':
                    request.POST=request.POST.copy()
                    form = Netflowform(request.POST)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+username)
                    else:
                        return render(request,'addnetflow.html',{'error':'提交的数据可能存在异常，客户信息无法创建'})
                form = Netflowform(auto_id=False)
                form.fields['username'].initial = username
                return render(request,'addnetflow.html',{'form':form})
            if key == 'cacti':
                if request.method == 'POST':
                    request.POST=request.POST.copy()
                    form = Cactiform(request.POST)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+username)
                    else:
                        return render(request,'addcacti.html',{'error':'提交的数据可能存在异常，客户信息无法创建'})
                form = Cactiform(auto_id=False)
                form.fields['username'].initial = username
                return render(request,'addcacti.html',{'form':form})
            if key == 'availability':
                if request.method == 'POST':
                    request.POST=request.POST.copy()
                    form = Availabilityform(request.POST)
                    if form.is_valid():
                        form.save()
                        return HttpResponseRedirect('/account/'+username)
                    else:
                        return render(request,'addavailability.html',{'error':'提交的数据可能存在异常，客户信息无法创建'})
                form = Availabilityform(auto_id=False)
                form.fields['username'].initial = username
                return render(request,'addavailability.html',{'form':form})
            return render(request,'page-error-404.html')
        else:
            return render(request,'page-error-404.html')
    return render(request,'page-login.html')

def menu(request,menu): 
    '''
    @todo:客户页操作菜单，非菜单内容的页面返回404
    '''
    if request.user.is_authenticated:
        if menu == 'cacti':
            q = request.user.username
            lines = Cacti.objects.filter(username=q)
            if lines:
                menu_cacti_id = 0
                if 'mcid' in request.GET:
                    menu_cacti_id = request.GET['mcid']
                image_url = ''
                if lines[int(menu_cacti_id)].server == 'cacti1':
                    image_url = 'http://mrtg.fnetlink.com.hk:10080/graph_image1.php?local_graph_id='+lines[int(menu_cacti_id)].graphid
                elif lines[int(menu_cacti_id)].server == 'cacti2':
                    image_url = 'http://202.173.255.28:10080/cacti/graph_image1.php?local_graph_id='+lines[int(menu_cacti_id)].graphid
                elif lines[int(menu_cacti_id)].server == 'cacti3':
                    image_url = 'http://mrtg3.fnetlink.com.hk:10080/graph_image1.php?local_graph_id='+lines[int(menu_cacti_id)].graphid
                line_desc = lines[int(menu_cacti_id)].description
                url = request.path
                return render(request,'cacti.html',{'lines':lines, 'image_url':image_url, 'line_desc':line_desc, 'url':url})
            else:
                return render(request,'cacti.html')
        elif menu == 'availability':
            q = request.user.username
            availObjs = Availability.objects.filter(username=q)
            if availObjs:
                lines = []
                for avail in availObjs:
                    key = {}
                    url = 'http://202.104.174.177:10088/zabbix/dixonx.php?triggerid='+avail.triggerid
                    value = str(urllib.request.urlopen(url).read(),encoding='utf-8').split('---')
                    key['ip'] = avail.ip
                    key['description'] = avail.description
                    key['thisMonthDown'] = value[0]
                    key['thisMonthSLA'] = value[1]
                    key['lastMonthDown'] = value[2]
                    key['lastMonthSLA'] = value[3]
                    lines.append(key)
                return render(request,'availability.html',{'lines':lines})
            else:
                return render(request,'availability.html')
        elif menu == 'sla':
            today = datetime.date.today()
            last_month = datetime.date(day=1,month=today.month-1,year=today.year).strftime('%Y_%m')
            if 'latency' in request.GET:
                title = '-Latency'
                url = 'https://portal.dyxnet.com/ClientPortal/client_portal/SLAData/'+last_month+'/gold_1.gif'
            elif 'loss' in request.GET:
                title = '-Packet Loss Rate'
                url = 'https://portal.dyxnet.com/ClientPortal/client_portal/SLAData/'+last_month+'/gold_2.gif'
            elif 'jlitter' in request.GET:
                title = '-Jlitter'
                url = 'https://portal.dyxnet.com/ClientPortal/client_portal/SLAData/'+last_month+'/gold_3.gif'
            else:
                return render(request,'page-error-404.html')
            return render(request,'sla.html',{'url':url,'title':title})
        elif menu == 'nflow':
            q = request.user.username
            try:
                netflow = Netflow.objects.get(username=q)
                url = ''
                if netflow.server == 'netflow1':
                    url = 'http://mrtg.fnetlink.com.hk:28080/netflow/jspui/NetworkSnapShot.jsp?'
                elif netflow.server == 'netflow2':
                    url = 'http://211.148.131.43:18080/netflow/jspui/index.jsp?'
                elif netflow.server == 'netflow3':
                    url = 'http://202.104.174.177:28088/netflow/jspui/NetworkSnapShot.jsp?'
                return render(request,'nflow.html',{'netflow':netflow,'url':url})
            except:
                return render(request,'nflow.html')
        elif menu == 'report':
            q = request.user.username
            fileurl = Report.objects.filter(username=q)
            return render(request,'report.html',{'fileurl':fileurl})
        return render(request,'page-error-404.html')
    return HttpResponseRedirect('/login/')
