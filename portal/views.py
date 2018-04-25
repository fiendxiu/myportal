from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login_view(request):
    error = True
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')
        else:
            return render(request,'page-login.html',{'error':error})
    return render(request,'page-login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@csrf_exempt
def reset_passwd(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user,request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
        form = PasswordChangeForm(user=request.user)
        return render(request,'changepass.html',{'form':form})
    errors = "你好像无权访问吧?"
    return render(request,'page-error-404.html')

@csrf_exempt
def index(request):
#    if request.user.is_authenticated:
#            return render(request,'index.html')
#    return HttpResponseRedirect('/login/')
    return render(request,'index.html')

def menu(request,menu): 
    #assert False
    if menu=='/':
        return render(request,'index.html')
    elif menu=='cacti/':
        return render(request,'cacti.html')
    elif menu=='sla/':
        return render(request,'sla.html')
    elif menu=='nflow/':
        return render(request,'nflow.html')
    elif menu=='report/':
        return render(request,'report.html')
    return render(request,'index.html')


