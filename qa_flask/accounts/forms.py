# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/23 
"""
import hashlib

from flask import request
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from models import User, db, UserProfile, UserLoginHistory
from utils import constants
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    """用户注册"""
    # render_kw：书写html属性
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[DataRequired('请输入用户名'), phone_required])
    nickname = StringField(label='用户昵称', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入昵称'
    }, validators=[DataRequired('请输入昵称'), Length(min=2, max=20, message='昵称长度在2-20间')])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('请输入密码')])
    confirm_password = PasswordField(label='确认密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请重复密码'
    }, validators=[DataRequired('请重复密码'), EqualTo(fieldname='password', message='2次密码输入不一致')])

    def validate_username(self, field):
        """检测用户名是否已存在"""
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('此用户名已注册')
        return field

    def register(self):
        """用户注册函数"""
        # 获取表单信息
        username = self.username.data
        password = self.password.data
        nickname = self.nickname.data
        # 添加到db.session
        try:
            # 将密码加密存储
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, password=password, nickname=nickname)
            db.session.add(user_obj)
            profile = UserProfile(username=username, user=user_obj)
            db.session.add(profile)
            db.session.commit()
            # 跳转到成功页面
            return user_obj
        except Exception as e:
            print(e)
        return None


class LoginForm(FlaskForm):
    """用户登录"""
    # render_kw：书写html属性
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[DataRequired('请输入用户名'), phone_required])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('请输入密码')])

    def validate(self):
        """用户登录验证"""
        result = super().validate()
        username = self.username.data
        password = self.password.data
        if result:
            # TODO 验证加密后的密码是否正确
            user = User.query.filter_by(username=username, password=password).first()
            # print('用户：', user)
            if user is None:
                result = False
                self.username.errors = ['用户名或密码错误']
            elif user.status == constants.UserStatus.USER_INACTIVE.value:
                result = False
                self.username.errors = ['用户已禁用']
        return result

    def do_login(self):
        """执行登录逻辑"""
        username = self.username.data
        password = self.password.data
        try:
            # 查找对应的用户
            # TODO 验证加密后的密码是否正确
            user = User.query.filter_by(username=username, password=password).first()
            # 登录用户
            # session['user_id'] = user.id
            login_user(user)
            # 记录日志
            ip = request.remote_addr
            ua = request.headers.get('user-agent', None)
            obj = UserLoginHistory(username=username, ip=ip, ua=ua, user=user)
            db.session.add(obj)
            db.session.commit()
            return user
        except Exception as e:
            print(e)
        return None
