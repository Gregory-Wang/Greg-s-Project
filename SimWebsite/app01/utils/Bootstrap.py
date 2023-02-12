"""
Bootstrap 的 ModelForm 父类

使用方法
# 1 导入 from app01.utils.Bootstrap import BootstrapModelForm
# 2 创建 ModelForm 类并继承 BootstrapModelForm
    例如：
    # 用户管理
    class UserModelForm(BootstrapModelForm):
        class Meta:
            model = models.UserInfo
            fields = ["name", "password", "age", "salary", "create_time", "gender", "depart"]  # 自定义字段
            # fields = "__all__"  # 全部字段
            # exclude = ["name"]  # 排除字段

"""


from django import forms

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }

            # widgets = {
            #     "name": forms.TextInput(attrs={"class": "form-control"}),
            #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
            # }
            
            if name == 'password': field.widget.input_type = 'password'  # 密码隐藏
            if name == 'create_time': field.widget.input_type = 'date'  # 调用日期输入格式插件（存在编辑功能传不了默认值的bug）
