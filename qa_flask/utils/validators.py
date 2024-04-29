# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/23 
"""
import re

from wtforms import ValidationError


def phone_required(form, field):
    """自定义售价后面验证"""
    # 强制验证用户名为手机号
    username = field.data
    pattern = r'^1[0-9]{10}$'
    if not re.search(pattern, username):
        raise ValidationError('请输入手机号')
    return field
