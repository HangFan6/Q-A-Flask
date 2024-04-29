# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/23 
"""
from datetime import datetime

import timeago


def number_split(num):
    """
    数字千分位格式化：123465.562 => 123,465.562
    :param num: 需要格式化的数字
    :return:格式化后的字符串
    """
    return '{:,}'.format(int(num))


def dt_format_show(dt):
    """
    日期和时间，格式化显示：
    :param dt:时间
    :return:xx分钟/小时前
    """
    now = datetime.now()
    return timeago.format(dt, now, 'zh_CN')
