# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/21
"""
import os


class Config(object):
    """ 项目的配置文件 """
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ht103066@localhost/flask_qa'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flash, form wtf
    SECRET_KEY = 'abcdsacb12312'
    # 文件上传的根路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'medias')
