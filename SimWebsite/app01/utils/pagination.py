"""
*********************
自定义分页组件
*********************

# 使用方法

> views.py
1 导入 pagination.py 包
    from app01.utils.pagination import Pagination

2 获取靓号表数据
    # 该行代码相当于: select * from 表 order by 表头 desc(-) / asc(+)
    # 可以实现按顺序排列
    xxx_table = models.PrettyNum.objects.filter(**data_dict).order_by("b表头")

3 实例化 Pagination 方法，传入参数 request、queryset
    page_object = Pagination(request, xxx_table)
    page_queryset = page_object.page_queryset

4 传递数据，添加 number_table 和 page_string
    return render(request, "xxx.html" ,{
            'xxx_table' : page_object.page_queryset,      # 分完页的数据
            "page_string": page_object.pageCounting(),    # 页码
            })

> xxx.html
添加分页组件
    <nav aria-label="Page navigation">
        <ul class="pagination">
            {{ page_string }}
        </ul>
    </nav>

"""
from django.utils.safestring import mark_safe
""" django从view向template传递HTML字符串的时候, django默认不渲染此HTML, 原因是为了防止这段字符串里面有恶意攻击的代码。
mark_safe这个函数就是确认这段函数是安全的, 不是恶意攻击的 """
import copy

class Pagination(object):

    """
    page: 当前页数
    page_params: （设置）当前页数
    page_size: （设置）单个页面显示多少数据
    plus: (设置)前后显示多少页

    queryset 接收对应的 xxx_table 参数

    """

    def __init__(self, request, queryset, page_size=5, page_params="page", plus=5):
        page = request.GET.get(page_params, "1")  # "1"为默认值

        # 拼接 url 使检索和页码功能相兼容
        # 复制一份 url
        query_dict = copy.deepcopy(request.GET)
        # 使 url 可修改
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_params = page_params

        # 判断当前页码字符串是否为十进制数
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page

        # 分页起始位置
        self.page_start = (page - 1) * page_size
        self.page_end = page * page_size
        self.page_queryset = queryset[self.page_start:self.page_end]

        # 数据总条数
        total_count = queryset.count()

        # 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus
    
    def pageCounting(self):
        # 计算出当前页的前n页和后n页
        if self.total_page_count <= 2 * self.plus + 1:
            # 当数据库中的数据较少时（没有达到2n+1页）
            start_page = 1
            end_page = self.total_page_count
        else:
            # 当数据库中的数据较多时（多于2n+1）

            # 当前页数小于n
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页数 > n
                # 当前页数+n > 总页数
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.age - self.plus
                    end_page = self.page + self.plus

        
        # 页码
        page_str_list = []
        # 修改 url 的 page（page_params）为 1
        self.query_dict.setlist(self.page_params, [1])
        # page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_params, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_params, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_params, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        
        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_params, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_params, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        search_string = """
        <li>
            <form style="float: left; margin-left: -1px" method="get">
                <input name="page" style="position: relative; display: inline-block; width: 80px; border-radius: 4px;"
                        type="text" class="form-control" placeholder="页码">
                <button style="border-radius: 4px;" class="btn btn-default" type="submit">跳转</button>
            </form>
        </li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string