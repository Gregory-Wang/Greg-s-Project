from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.exceptions import ValidationError

from app01.utils.pagination import Pagination
from app01.utils.Bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5

class AdminModelForm(BootstrapModelForm):

    # 单独添加“确认密码”
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,

        # （render_value）验证错误后不清空输入框
        # widget=forms.PasswordInput(render_value=True)
        )
        
    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
    
    # 调用 encrypt.py 执行 md5 加密
    def clean_password(self):
        orig_pwd = self.cleaned_data.get('password')
        return md5(orig_pwd)

    # 验证确认密码的清理方法，参考下面文档
    # https://docs.djangoproject.com/zh-hans/4.1/ref/forms/validation/
    # clean_xxx 其中xxx为要验证并保存的字段
    def clean_confirm_password(self):
        # print(self.cleaned_data)
        orig_pwd = self.cleaned_data.get('password')
        conf_pwd = md5(self.cleaned_data.get('confirm_password'))
        # print(self.cleaned_data)
        # print(orig_pwd, conf_pwd)
        if conf_pwd != orig_pwd:
            raise ValidationError("密码不一致，请重新输入")
        return conf_pwd  # 返回什么，该字段保存到数据库的值就是什么（进入 form）

class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]

class AdminResetModelForm(BootstrapModelForm):

    # 单独添加“确认密码”
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,

        # （render_value）验证错误后不清空输入框
        # widget=forms.PasswordInput(render_value=True)
        )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
    
    # 调用 encrypt.py 执行 md5 加密
    def clean_password(self):
        orig_pwd = self.cleaned_data.get('password')
        chec_pwd = md5(orig_pwd)
        # 去数据库校验当前密码和新输入密码是否重复（pk 指的是 primary key，即主键）
        exists = models.Admin.objects.filter(id=self.instance.pk, password=chec_pwd).exists
        if exists:
            raise ValidationError("密码不能与之前的相同")
        return md5(orig_pwd)

    # 验证确认密码的清理方法，参考下面文档
    # https://docs.djangoproject.com/zh-hans/4.1/ref/forms/validation/
    # clean_xxx 其中xxx为要验证并保存的字段
    def clean_confirm_password(self):
        # print(self.cleaned_data)
        orig_pwd = self.cleaned_data.get('password')
        conf_pwd = md5(self.cleaned_data.get('confirm_password'))
        if conf_pwd != orig_pwd:
            raise ValidationError("密码不一致，请重新输入")
        return conf_pwd  # 返回什么，该字段保存到数据库的值就是什么
    



def admin_list(request):
    """ 管理员列表 """

    # 关键词检索功能
    # 创建一个空字典（默认搜索关键词为空）
    data_dict = {}
    search_data = request.GET.get('q','')  # 搜索框默认值预览，有值取q，没值取空字符串
    if search_data:
        data_dict["username__contains"] = search_data  # xxx__contains 的xxx为检索列头

    # 搜索条件
    admin_table = models.Admin.objects.filter(**data_dict).all()

    # 分页
    page_object = Pagination(request, admin_table)
    page_queryset = page_object.page_queryset

    return render(request, "admin_list.html" ,{
            'active_menu': 'admin_list',                 #
            'data_table': page_queryset,                 #
            "page_string": page_object.pageCounting(),   # 页码
            'search_data' : search_data,                 # 检索数据
            })

def admin_add(request):
    """ 添加管理员 """

    title = "新建管理员"
    
    if request.method == 'GET':
        
        form = AdminModelForm()
        return render(request, "change.html", {
            "title": title,    # 公共添加页面的标题参数
            "form": form,
            })
    
    # 获取用户 POST 提交过来的数据，并进行数据校验
    form = AdminModelForm(data=request.POST)
    if form.is_valid():  # 逐一对 UserModelForm 内的字段进行校验
        # 数据合法
        # print(form.cleaned_data)
        # 保存到数据库 UserInfo（UserModelForm 内 Meta 定义的数据库表）
        form.save()  # save() 为添加数据，非 update，此处添加数据和后面的修改数据实现方法有出入
        return redirect("/admin/list/")
    return render(request, "change.html", {
            "title": title,    # 公添加页面的标题参数
            "form": form,
            })


def admin_edit(request, nid):
    """ 编辑管理员 """

    title = "编辑管理员"

    # 根据 nid 获取与选中项相应的数据
    row_object = models.Admin.objects.filter(id=nid).first()

    # 判断 nid 是否存在
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在"})
    
    if request.method == 'GET':
        # 实例化 ModelForm
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {
            "title": title,
            "form": form,
        })
    
    # 获取用户 POST 提交过来的数据，并进行数据校验
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 逐一对 UserModelForm 内的字段进行校验
        # 数据合法
        # print(form.cleaned_data)
        # 保存到数据库 UserInfo（UserModelForm 内 Meta 定义的数据库表）
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {
            "title": title,
            "form": form,
        })

def admin_delete(request, nid):
    """ 删除管理员 """

    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")

def admin_reset(request, nid):
    """ 重置密码 """

    row_object = models.Admin.objects.filter(id=nid).first()
    # 判断 nid 是否存在
    if not row_object:
        return render(request, 'error.html', {"msg": "数据不存在"})
    title = "重置管理员密码 - {}".format(row_object.username)

    if request.method == 'GET':
        
        form = AdminResetModelForm()
        return render(request, 'change.html', {
                "title": title,
                "form": form,
            })

    # 获取用户 POST 提交过来的数据，并进行数据校验
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 逐一对 UserModelForm 内的字段进行校验
        # 数据合法
        # print(form.cleaned_data)
        # 保存到数据库 UserInfo（UserModelForm 内 Meta 定义的数据库表）
        form.save()  # save() 为添加数据，非 update，此处添加数据和后面的修改数据实现方法有出入
        return redirect("/admin/list/")
    return render(request, "change.html", {
            "title": title,    # 公共添加页面的标题参数
            "form": form,
            })