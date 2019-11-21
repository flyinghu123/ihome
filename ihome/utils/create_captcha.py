#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-11-21 22:54:30
# @Author  : Flying Hu (1152598046@qq.com)
# @Link    : http://www.flyinghu.cn/
# @Version : $Id$

from captcha.image import ImageCaptcha
from io import BytesIO
import os
import random
import string

# characters为验证码上的字符集，10个数字加26个大写英文字母
# 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ str类型
characters = string.ascii_letters + string.digits
width, height, n_len, n_class = 170, 80, 4, len(characters)
# 字体列表
# fonts = ['./font/MICROSS.TTF', './font/msyh.ttc', './font/msyhbd.ttc', './font/msyhl.ttc']
# 设置验证码图片的宽度widht和高度height
# 除此之外还可以设置字体fonts和字体大小font_sizes
# generator = ImageCaptcha(width=width, height=height, fonts=fonts)
generator = ImageCaptcha(width=width, height=height)


def create_image_code(code_str=None, fmt='PNG', path=None):
    """Create a captcha.

    Args:
        path: save path, default None.
        fmt: image format, PNG / JPEG.
    Returns:
        A tuple, (code_str, StringIO.value).
        For example:
            ('JGW9', '\x89PNG\r\n\x1a\n\x00\x00\x00\r...')

    """
    if not code_str:
        code_str = ''.join([random.choice(characters) for j in range(4)])
    # 生成验证码
    img = generator.generate_image(str(code_str))
    # 保存验证码
    out = BytesIO()
    img.save(out, format=fmt)
    if path:
        img.save(os.path.join(path, code_str) + '.' + fmt.lower(), fmt)
    return code_str, out.getvalue()


if __name__ == '__main__':
    # create_verify_code_images(1000000)
    print(create_image_code())
