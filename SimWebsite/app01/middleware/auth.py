"""
*********************
中间件
*********************

# 使用方法
  # 1 在 settings.py 中的 MIDDLEWARE 里注册中间件：
    MIDDLEWARE = [
        ***
        'app01.middleware.auth.M1',
        'app01.middleware.auth.M2',
    ]
    *注意：中间件的顺序由填写顺序决定，谁在前面先执行谁
  # 2 

"""


from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

class AuthMiddleware(MiddlewareMixin):
    """ 中间件1 """

    # process_request 若无返回值（即返回 None），可直接通过
    # 如果 M1 有返回值，如 HttpResponse、render、redirect 等则直接走 M1 的 process_response，不予继续向后执行
    def process_request(self, request):

        # 0 排除不需要验证的页面
        # request.path_info 可获取当前用户请求的 url
        # if request.path_info == "/login/":
        if request.path_info in ["/login/", "/image/code/"]:
            return  # 返回空值，允许继续前进

        # 1 读取当前访问用户的 session 信息
        # 若能读取成功，说明用户已经登录，则可继续往前走（返回空值）
        info_dict = request.session.get("info")
        if info_dict:
            return
        
        # 2 没有登录过，则回到登录页面
        return redirect('/login/')
