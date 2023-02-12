"""
python manage.py makemigrations    
python manage.py migrate
"""

from django.db import models

# Create your models here.

class Admin(models.Model):
    """ 管理员表 """
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)

    # 重写了函数，实例化对象时输出的是地址，__str__(self)可以打印具体的属性
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    # (备注, 数字长度, 小数位, 默认值)
    salary = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')  # 只包含年月日

    # 元组
    # Django 中做的约束，写性别时只能写1或2
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    # 外键
    # depart_id = models.BigIntegerField(verbose_name='部门id')

    # 外键约束
    # to 与哪张表关联
    # to_field 表中的哪一列关联
    # depart = models.ForeignKey(to="Department", to_field="id")

    # 若部门表中的某个部门被删除，则员工表内的相关员工有两种情况：
    # 级联删除 on_delete=models.CASCADE
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # 将部门ID制空（且让表允许为空）
    depart = models.ForeignKey(verbose_name='部门', to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格", default=0)
    # 允许为空请添加 null=True, blank=True
    level_choices = {
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    }
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = {
        (1, "已占用"),
        (2, "未占用")
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)

