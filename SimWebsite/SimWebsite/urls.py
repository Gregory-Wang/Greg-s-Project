"""SimWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from app01 import views
from app01.views import depart, user, number, admin

urlpatterns = [
    #path('admin/', admin.site.urls),

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),  # <int:nid> 正则表达式，传递 nid 到 views

    # 用户管理
    path('user/list/', user.user_list),
    path('user/<int:nid>/edit/', user.user_edit),  # <int:nid> 正则表达式，传递 nid 到 views
    path('user/<int:nid>/delete/', user.user_delete),  # <int:nid> 正则表达式，传递 nid 到 views

    # 靓号管理
    path('number/list/', number.number_list),
    path('number/<int:nid>/edit/', number.number_edit),  # <int:nid> 正则表达式，传递 nid 到 views
    path('number/<int:nid>/delete/', number.number_delete),  # <int:nid> 正则表达式，传递 nid 到 views

    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/', admin.admin_add),
]
