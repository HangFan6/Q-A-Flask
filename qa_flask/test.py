# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/24 
"""
import time
import datetime

now = datetime.datetime.now()
print(now)

# 获取当前时间戳
timestamp = int(time.time())
print(timestamp)

# 获取当前日期和时间
timestamp = int(time.time())
now = time.strftime("%Y-%m-%d#%H:%M:%S-", time.localtime(timestamp))
print(now)
print(type(now))
