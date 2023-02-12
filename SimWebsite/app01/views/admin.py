from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.exceptions import ValidationError

from app01.utils.pagination import Pagination
from app01.utils.Bootstrap import BootstrapModelForm
from app01.utils.encrypt import md5

class AdminModelForm(BootstrapModelForm):

    # 单独添加“确认密码”
    confirm_passowrd = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,

        # （render_value）验证错误后不清空输入框
        # widget=forms.PasswordInput(render_value=True)
        )
        
    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_passowrd"]
    
    # 调用 encrypt.py 执行 md5 加密
    def clean_password(self):
        orig_pwd = self.cleaned_data.get('password')
        return md5(orig_pwd)

    # 验证确认密码的清理方法，参考下面文档
    # https://docs.djangoproject.com/zh-hans/4.1/ref/forms/validation/
    # clean_xxx 其中xxx为要验证并保存的字段
    def clean_confirm_passowrd(self):
        print(self.cleaned_data)
        orig_pwd = self.cleaned_data.get('password')
        conf_pwd = md5(self.cleaned_data.get('confirm_passowrd'))
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
        return render(request, "item_adding.html", {
            "title": title,    # 公共添加页面的标题参数
            "form": form,
            })
    
    # 获取用户 POST 提交过来的数据，并进行数据校验
    form = AdminModelForm(data=request.POST)
    if form.is_valid():  # 逐一对 UserModelForm 内的字段进行校验
        # 数据合法
        print(form.cleaned_data)
        # 保存到数据库 UserInfo（UserModelForm 内 Meta 定义的数据库表）
        form.save()  # save() 为添加数据，非 update，此处添加数据和后面的修改数据实现方法有出入
        return redirect("/admin/list/")
    return render(request, "item_adding.html", {
            "title": title,    # 公共添加页面的标题参数
            "form": form,
            })

        