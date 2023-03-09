"""
*********************
图片验证码生成

参考：
https://www.cnblogs.com/wupeiqi/articles/5812291.html
*********************

# 使用方法
  # 1 在中间件 auth.py 中添加验证排除
    def process_request(self, request):
        if request.path_info in ["/login/", "/image/code/"]:
            return

  # 2.1 在视图函数中引用 code.py 的 check_code 和方法以及 BytesIO
    from app01.utils.code import check_code
    from io import BytesIO

  # 2.2 在视图函数中添加图片验证码生成的函数
    def image_code(request):
        # 生成图片验证码

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

  # 3 在 html 页面嵌入 url
    <div class="col-xs-5">
        <img id="image_code" src="/image/code/">
    </div>

"""

import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def check_code(width=120, height=30, char_length=4, font_file='kumo.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')
 
    def rndChar():
        """
        生成随机字母   
        :return:
        """
        return chr(random.randint(65, 90))
 
    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))
 
    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())
 
    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
 
    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())
 
    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
 
        draw.line((x1, y1, x2, y2), fill=rndColor())
 
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img,''.join(code)

# if __name__ == '__main__':

#     img, code_str = check_code()
#     print(code_str)

#     with open('code.png','wb') as f:
#         img.save(f,format='png')