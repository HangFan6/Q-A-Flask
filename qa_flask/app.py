from flask import Flask, session, g
from flask_ckeditor import CKEditor
from flask_login import LoginManager

from accounts.views import accounts
from models import db, User
from qa.views import qa
from utils.filters import number_split, dt_format_show

app = Flask(__name__, static_folder='medias')
app.config.from_object('conf.Config')

# 数据库初始化
db.init_app(app)
app_ctx = app.app_context()
app_ctx.push()

# 富文本初始化
ckeditor = CKEditor(app)
# ckeditor = CKEditor()
# ckeditor.init_app(app)

# 登录验证
login_manager = LoginManager()
login_manager.login_view = 'accounts.login'
login_manager.login_message = '请登录'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(qa, url_prefix='/')

# 注册过滤器
app.jinja_env.filters['number_split'] = number_split
app.jinja_env.filters['dt_format_show'] = dt_format_show


# @app.before_request
# def before_request():
#     """如果有用户id，设置到全局对象"""
#     user_id = session.get('user_id', None)
#     if user_id:
#         user = User.query.get(user_id)
#         # print(user)
#         g.current_user = user


# 使用flask-login验证用户
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
