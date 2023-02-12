"""
*********************
md5加密
*********************

# 使用方法
  # 1 基础方法：直接调用
  md5(xxx)

  # 2 进阶方法：编写钩子函数
  def clean_password(self):
        orig_pwd = self.cleaned_data.get('password')
        return md5(orig_pwd)

"""
from django.conf import settings
import hashlib

def md5(data_string):
    # 借用 Django settings.py 内的随机生成的 SECRET_KEY 当作盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()

