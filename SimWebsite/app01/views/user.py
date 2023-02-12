from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.Bootstrap import BootstrapModelForm

# 用户管理
class UserModelForm(BootstrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "salary", "create_time", "gender", "depart"]  # 自定义字段
        # fields = "__all__"  # 全部字段
        # exclude = ["name"]  # 排除字段
    
def user_list(request):
    """ 用户列表 """

    if request.method == 'GET':
        # 实例化 ModelForm
        form = UserModelForm()

        # 2 获取靓号表数据
        # 该行代码相当于: select * from 表 order by 表头 desc(-) / asc(+)
        # 可以实现按顺序排列
        user_table = models.UserInfo.objects.all()

        # 实例化 Pagination 方法，传入参数 request、queryset
        page_object = Pagination(request, user_table)
        page_queryset = page_object.page_queryset

        # 获取所有的用户列表 (旧)
        # queryset = models.UserInfo.objects.all()
        # for obj in queryset:
            # print(obj.id, obj.name, obj.password, obj.age, obj.salary, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.depart)
            # print(obj.id, obj.name, obj.password, obj.age, obj.salary, obj.create_time.strftime("%Y-%m-%d"), obj.get_gender_display(), obj.depart.title)

        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }

        return render(request, 'user_list.html', {
            # 'queryset': queryset,
            'context': context,
            'form': form,
            'active_menu': 'user_list',
            'user_table' : page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.pageCounting(),    # 页码
            })

    # 获取用户 POST 提交过来的数据，并进行数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():  # 逐一对 UserModelForm 内的字段进行校验
        # 数据合法
        print(form.cleaned_data)
        # 保存到数据库 UserInfo（UserModelForm 内 Meta 定义的数据库表）
        form.save()  # save() 为添加数据，非 update，此处添加数据和后面的修改数据实现方法有出入
        return redirect("/user/list/")
    else:
        # 校验失败
        print(form.errors)

    return redirect("/user/list/")

def user_edit(request,nid):
    """ 修改用户 """
    # 根据 nid 到数据库中获取要编辑的那一行数据(对象instance=row_object)
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 实例化 ModelForm
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form, 'active_menu': 'user_list',})
    

    # 获取用户 POST 提交过来的数据，并进行数据校验
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 逐一对 UserModelForm 内的字段进行校验
        # 数据合法
        print(form.cleaned_data)
        # 保存到数据库 UserInfo（UserModelForm 内 Meta 定义的数据库表）
        form.save()
        return redirect("/user/list/")
    else:
        # 校验失败
        print(form.errors)

def user_delete(request, nid):
    """ 删除用户 """

    # 删除
    models.UserInfo.objects.filter(id=nid).delete()

    # 重定向回主页
    return redirect("/user/list/")
