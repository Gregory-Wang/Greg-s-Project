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
from app01.views import depart, user, number, admin, account, task, order

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
    path('admin/<int:nid>/edit/', admin.admin_edit),
    path('admin/<int:nid>/delete/', admin.admin_delete),
    path('admin/<int:nid>/reset/', admin.admin_reset),

    # 账户登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 任务管理
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),
    path('task/<int:nid>/edit/', task.task_edit),
    path('task/<int:nid>/delete/', task.task_delete),

    # 订单
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/edit/', order.order_edit),
    path('order/delete/', order.order_delete),
]
