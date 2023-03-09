import json
from django.shortcuts import render, redirect, HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.Bootstrap import BootstrapModelForm


class TaskModelForm(BootstrapModelForm):

    class Meta():
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput
        }

def task_list(request):
    """ 任务列表 """

    form = TaskModelForm()

    # 关键词检索功能
    # 创建一个空字典（默认搜索关键词为空）
    data_dict = {}
    search_data = request.GET.get('q','')  # 搜索框默认值预览，有值取q，没值取空字符串
    if search_data:
        data_dict["title__contains"] = search_data  # xxx__contains 的xxx为检索列头

    # 搜索条件
    task_table = models.Task.objects.filter(**data_dict).all()

    # 分页
    page_object = Pagination(request, task_table)
    page_queryset = page_object.page_queryset

    return render(request, "task_list.html" ,{
            'active_menu': 'task_list',                 #
            'data_table': page_queryset,                 #
            "page_string": page_object.pageCounting(),   # 页码
            'search_data' : search_data,                 # 检索数据
            'form': form,
            })


@csrf_exempt  # 绕过安全认证
def task_add(request):
    """ 添加任务 """

    print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "error":form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

def task_edit(request, nid):
    """ 编辑任务 """

    title = "编辑任务"

    # 根据 nid 获取与选中项相应的数据
    row_object = models.Task.objects.filter(id=nid).first()

    # 判断 nid 是否存在
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在"})
    
    if request.method == 'GET':
        # 实例化 ModelForm
        form = TaskModelForm(instance=row_object)
        return render(request, 'change.html', {
            "title": title,
            "form": form,
        })
    
    # 获取用户 POST 提交过来的数据，并进行数据校验
    form = TaskModelForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 逐一对 UserModelForm 内的字段进行校验
        # 数据合法
        # print(form.cleaned_data)
        # 保存到数据库 UserInfo（UserModelForm 内 Meta 定义的数据库表）
        form.save()
        return redirect("/task/list/")
    return render(request, 'change.html', {
            "title": title,
            "form": form,
        })

def task_delete(request, nid):
    """ 删除任务 """

    models.Task.objects.filter(id=nid).delete()
    return redirect("/task/list/")