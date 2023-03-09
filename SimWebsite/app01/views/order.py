import json
import random
from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.Bootstrap import BootstrapModelForm



class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        # fields = [""]
        exclude = ["oid", "admin"]

def order_list(request):
    """ 订单列表 """

    form = OrderModelForm()

    # 关键词检索功能
    # 创建一个空字典（默认搜索关键词为空）
    data_dict = {}
    search_data = request.GET.get('q','')  # 搜索框默认值预览，有值取q，没值取空字符串
    if search_data:
        data_dict["title__contains"] = search_data  # xxx__contains 的xxx为检索列头

    order_table = models.Order.objects.filter(**data_dict).all().order_by('-id')

    # 分页
    page_object = Pagination(request, order_table)
    page_queryset = page_object.page_queryset

    return render(request, "order_list.html" ,{
            'active_menu': 'order_list',                 #
            'data_table': page_queryset,                 #
            "page_string": page_object.pageCounting(),   # 页码
            'search_data' : search_data,                 # 检索数据
            'form': form,
            })

@csrf_exempt
def order_add(request):
    """ 添加订单 """

    form = OrderModelForm(data=request.POST)
    if form.is_valid():

        # 订单号随机生成
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000,9999))
        # 固定生成管理员（从session中获取管理员id）
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    """ 删除任务 """

    # 获取ajax反馈的uid
    uid = request.GET.get('uid')
    # 判断uid是否存在（防止多用户同时进行删除操作出现错误）
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "数据不存在，删除失败"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

def order_edit(request):
    """ 编辑任务 """
    """ 方法一

    # 获取对应订单的uid
    uid = request.GET.get('uid')
    # 判断uid是否存在（对象）
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'error': "数据不存在，编辑失败"})
    # 从数据库获取行对象
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }
    }
    return JsonResponse(result)

    """
    # 方法二 （JSON无法序列化对象）
    # 获取对应订单的uid
    uid = request.GET.get('uid')
    # 判断uid是否存在（字典）
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在，编辑失败"})
    # 从数据库获取行对象
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)
