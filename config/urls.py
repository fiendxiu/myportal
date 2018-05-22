"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', views.index),
    re_path(r'^login/$', views.login_view),
    re_path(r'^logout/$', views.logout_view),
    re_path(r'^resetpasswd/(?P<username>\w+)/$', views.reset_passwd),
    re_path(r'^search/$', views.search),
    re_path(r'^active/(?P<username>\w+)/$', views.isActive),
    re_path(r'^account/(?P<username>\w+)/$', views.account),

    re_path(r'^(?P<menu>\w+)/$', views.menu),
    re_path(r'^delete/(?P<key>\w+)/(?P<username>\w+)/$',views.delete),
    re_path(r'^edit/(?P<key>\w+)/(?P<username>\w+)/$',views.edit),
    re_path(r'^add/(?P<key>\w+)/(?P<username>\w+)/$',views.add),
]
