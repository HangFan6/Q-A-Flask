# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/21 
"""
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, g
from flask_login import login_user, logout_user

from accounts.forms import RegisterForm, LoginForm
from models import User, UserLoginHistory, db

accounts = Blueprint('accounts', __name__,
                     template_folder='templates',
                     static_folder='../assets')


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录 """
    form = LoginForm()
    next_url = request.values.get('next', url_for('qa.index'))
    if form.validate_on_submit():
        # print('正在登录')
        user = form.do_login()
        if user:
            # 跳转首页
            # flash('{}，欢迎回来！'.format(user.nickname), 'success')
            # return redirect(url_for('qa.index'))
            return redirect(next_url)
        else:
            flash('登录失败，请稍后重试', 'danger')
    # else:
    #     print(form.errors)
    return render_template('login.html', form=form, next_url=next_url)


@accounts.route('/logout')
def logout():
    """退出登录"""
    # # 自定义逻辑登录
    # session['user_id'] = ''
    # g.current_user = None
    logout_user()
    flash('欢迎下次再来！', 'success')
    return redirect(url_for('accounts.login'))


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    """ 注册 """
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register()
        if user_obj:
            # 跳转到成功页面
            flash('注册成功，请登录', 'success')
            return redirect(url_for('accounts.login'))
        else:
            flash('注册失败，请稍后重试', 'danger')
    return render_template('register.html', form=form)


@accounts.route('/mine')
def mine():
    """ 个人中心 """
    return render_template('mine.html')
