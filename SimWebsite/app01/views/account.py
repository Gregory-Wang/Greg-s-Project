from django.shortcuts import render, redirect, HttpResponse
from django import forms
from io import BytesIO

from app01 import models
from app01.utils.encrypt import md5
from app01.utils.code import check_code

class LoginForm(forms.Form):

    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": 'form-control'}),
        required=True  # 不能为空
    )
    password = forms.CharField(
        label="密码",
        # render_value=True 为不清空密码框
        widget=forms.PasswordInput(attrs={"class": 'form-control'}, render_value=True),
        required=True  # 不能为空
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class": 'form-control'}),
        required=True  # 不能为空
    )

    def clean_password(self):
        orig_pwd = self.cleaned_data.get('password')
        return md5(orig_pwd)

def login(request):
    """ 登录 """

    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到用户名和密码（form.cleaned_data）
        # print(form.cleaned_data)

        # * 验证码验证
        # pop() 用于及时清除 cleaned_data 中的验证码字段，防止后面用户名密码在数据库校验时出问题
        user_input_code = form.cleaned_data.pop('code')
        # 获取验证码或者空字符
        code = request.session.get('image_code', "")
        # 默认大写化
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # * 去数据库校验用户名和密码是否正确
        # 用解包的方式传字典进行验证（前提是 cleaned_data 字典里的键（即 LoginForm 里定义的字段名）要和数据库里（models.py）的字段相匹配）
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        # admin_object = models.Admin.objects.filter(username=form.cleaned_data['username'], password=form.cleaned_data['password']).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")  # 添加新报错到 form 里并显示在字段 password 上
            # form.add_error("username", "用户名或密码错误")  # 添加新报错到 form 里并显示在字段 username 上
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串（这里是用户的 id 和用户名合在一起的字典）；写到用户浏览器的 cookie 中；再写入到 session 中
        # 可在浏览器开发人员工具中查到 cookie 中加密过的 session info；在数据库中可以查到对应的内容
        request.session["info"] = {'id': admin_object.id, 'username': admin_object.username}
        # 登录成功后给 session 设置 7 天超时
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect("/admin/list")
    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    # 创建图片对象
    img, code_string = check_code()
    # print(code_string)

    # 将验证码字符串写入到 session 中（以便后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给 session 设置 60s 超时
    request.session.set_expiry(60)

    # 写入内存
    stream = BytesIO()
    img.save(stream, 'png')
    
    return HttpResponse(stream.getvalue())

def logout(request):
    """ 注销 """

    request.session.clear()
    return redirect('/login/')

