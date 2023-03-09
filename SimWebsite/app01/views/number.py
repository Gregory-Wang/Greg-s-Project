from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.pagination import Pagination
from app01.utils.Bootstrap import BootstrapModelForm

# 靓号管理
# 创建 ModelForm 类
class NumberModelForm(BootstrapModelForm):

    # 数据校验方法一：手机号验证————通过正则表达式实现
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1\d{10}$', '手机号格式错误')]
    # )

    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]# 自定义字段
        # fields = "__all__"  # 全部字段
        # exclude = ["name"]  # 排除字段
    
    # # 数据校验方法二：
    # def clean_mobile(self):
    #     input_mobile = self.cleaned_data["mobile"]
    #     if len(input_mobile) != 11:
    #         # 验证不通过
    #         raise ValidationError("格式错误：号码不足11位")
    #     # 验证通过，返回用户输入的值
    #     return input_mobile

    # 数据库中查询是否存在相同手机号
    def clean_mobile(self):
        input_mobile = self.cleaned_data["mobile"]
        
        exists = models.PrettyNum.objects.filter(mobile=input_mobile).exists()
        if exists:
            # 验证不通过
            raise ValidationError("手机号码已存在")
        # 验证通过，返回用户输入的值
        return input_mobile

# 创建继承 NumberModelForm 的 ModelForm 类
class NumberEditModelForm(NumberModelForm):

    # 数据校验方法一：手机号验证————通过正则表达式实现
    mobile = forms.CharField(
        # disabled=True,
        label="手机号",
        validators=[RegexValidator(r'^1\d{10}$', '手机号格式错误')]
    )

    # 数据库中查询是否存在相同手机号
    # 注意：要排除自己，否则无法原样保存
    def clean_mobile(self):
        input_mobile = self.cleaned_data["mobile"]
        # 获取当前行的 id 并在查询语句内排除掉：self.instance.pk
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=input_mobile).exists()
        if exists:
            # 验证不通过
            raise ValidationError("手机号码已存在")
        # 验证通过，返回用户输入的值
        return input_mobile

# 靓号列表页面
def number_list(request):
    ''' 靓号列表 '''

    # 关键词检索功能
    # 创建一个空字典（默认搜索关键词为空）
    data_dict = {}
    search_data = request.GET.get('q','')  # 搜索框默认值预览，有值取q，没值取空字符串
    if search_data:
        data_dict["mobile__contains"] = search_data

    if request.method == 'GET':
        # 1 实例化 ModelForm
        number_form = NumberModelForm()

        # 2 获取靓号表数据
        # 该行代码相当于：select * from 表 order by level desc(-) / asc(+)
        # 可以实现按顺序排列
        number_table = models.PrettyNum.objects.filter(**data_dict).order_by("level")

        # 3 分页功能
        # 实例化 Pagination 方法，传入参数 request、queryset
        page_object = Pagination(request, number_table)
        page_queryset = page_object.page_queryset

        # 4 获取 models.py 中的多选字段
        context = {
            'level_choices' : models.PrettyNum.level_choices,
            'status_choices' : models.PrettyNum.status_choices,
        }

        return render(request, "number_list.html" ,{
            'form' : number_form,                        # ModelForm 的实例化对象
            'active_menu': 'number_list',                # 导航栏当前选中状态
            'context' : context,                         # 级别和状态的多选数据
            'data_table' : page_object.page_queryset,    # 分完页的数据
            'search_data' : search_data,                 # 检索数据
            "page_string": page_object.pageCounting()    # 页码
            })

    # 获取用户 POST 提交过来的数据，并进行数据校验
    number_form = NumberModelForm(data=request.POST)
    if number_form.is_valid():  # 逐一对 NumberModelForm 内的字段进行校验
        # 数据合法
        print(number_form.cleaned_data)
        # 保存到数据库 NumberInfo（NumberModelForm 内 Meta 定义的数据库表）
        number_form.save()  # save() 为添加数据，非 update，此处添加数据和后面的修改数据实现方法有出入
        return redirect("/number/list/")
    else:
        # 校验失败
        print(number_form.errors)
    return redirect("/number/list/")


# 靓号修改页面
def number_edit(request, nid):
    """ 修改用户 """
    # 根据 nid 到数据库中获取要编辑的那一行数据(对象instance=row_object, 用于让编辑框显示默认值)
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        # 实例化 ModelForm
        number_form = NumberEditModelForm(instance=row_object)
        return render(request, "number_edit.html", {'active_menu': 'number_list', 'form': number_form})
    

    # 获取用户 POST 提交过来的数据，并进行数据校验
    number_form = NumberEditModelForm(data=request.POST, instance=row_object)
    if number_form.is_valid():  # 逐一对 NumberEditModelForm 内的字段进行校验
        # 数据合法
        print(number_form.cleaned_data)
        # 保存到数据库 PrettyNum（NumberEditModelForm 内 Meta 定义的数据库表）
        number_form.save()
        return redirect("/number/list/")
    else:
        # 校验失败
        print(number_form.errors)

    return render(request, "number_edit.html", {'active_menu': 'number_list', 'form': number_form})
    

# 靓号删除功能
def number_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    # 重定向回主页
    return redirect("/number/list/")