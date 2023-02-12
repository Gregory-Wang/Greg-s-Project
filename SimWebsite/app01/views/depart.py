from django.shortcuts import render, redirect
from app01 import models

# 部门管理
def depart_list(request):
    """ 部门列表 """
    # 去数据库中获取所有部门的列表
    # queryset 相当于列表
    queryset = models.Department.objects.all

    if request.method == 'GET':
        return render(request, 'depart_list.html', {'queryset': queryset, 'active_menu': 'depart_list',})

    # 获取用户 POST 提交过来的数据（title 输入为空）
    title = request.POST.get("depart-title")

    # 保存到数据库
    models.Department.objects.create(title=title)


    return redirect("/depart/list/")

def depart_delete(request):
    """ 删除部门 """
    # 1 获取ID
    nid = request.GET.get("nid")

    # 2 删除
    models.Department.objects.filter(id=nid).delete()

    # 3 重定向回主页
    return redirect("/depart/list/")

# http://127.0.0.1:8000/depart/1/list/
# http://127.0.0.1:8000/depart/nid/list/
def depart_edit(request,nid):
    """ 修改部门 """

    if request.method == "GET":
        # 根据 nid 获取数据
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object, 'active_menu': 'depart_list',})
    
    # 获取用户提交的标题
    title_new = request.POST.get('depart-title')

    # 根据 ID 找到数据库中对应的数据进行更新
    models.Department.objects.filter(id=nid).update(title=title_new)

    # 重定向回主页
    return redirect("/depart/list/")

