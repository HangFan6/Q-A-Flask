# -*-coding: Utf-8 -*-
"""
作者: HET
日期：2024/4/24 
"""
import os
import time

from flask import current_app
from flask_ckeditor import CKEditorField
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length

from models import Question, db, QuestionTags, Answer


class WriteQuestionForm(FlaskForm):
    """写文章/问题"""
    img = FileField(label='上传图片', render_kw={
        'accept': '.jpeg, .jpg, .png'
    }, validators=[
        FileAllowed(['jpeg', 'jpg', 'png'], '请选择合适的图片类型')
    ])
    title = StringField(label='标题', render_kw={
        'class': 'form-control',
        'placeholder': '请输入标题（最多50个字）'
    }, validators=[
        DataRequired('请输入标题'),
        Length(min=5, max=50, message='标题长度为5-50个字')
    ])
    tags = StringField(label='标签', render_kw={
        'class': 'form-control',
        'placeholder': '输入标签，用,分隔'
    })
    desc = TextAreaField(label='描述', render_kw={
        'class': 'form-control',
        'placeholder': '简述'
    }, validators=[Length(max=150, message='描述最长为150个字')])
    content = CKEditorField(label='文章内容', render_kw={
        'class': 'form-control',
        'placeholder': '请输入正文'
    }, validators=[
        DataRequired('请输入标题'),
        Length(min=5, message='正文内容不能少于5个字')])

    def save(self):
        """发布问题并保存"""
        # 获取图片
        img = self.img.data
        img_name = ''
        if img:
            # 需要在自定义配置与基本配置中，设置文件上传路径
            timestamp = int(time.time())
            now = time.strftime("%Y%m%d-%H%M%S-", time.localtime(timestamp))
            # 按日期保存图片
            img_name = secure_filename(now + img.filename)  # 设置图片安全名称
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        # 保存问题
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        que_obj = Question(
            title=title,
            desc=desc,
            img=img_name,
            content=content,
            user=current_user
        )
        db.session.add(que_obj)
        db.session.commit()
        # 保存标签-
        tags = self.tags.data
        for tag_name in tags.split('，'):
            if tag_name:
                tag_obj = QuestionTags(tag_name=tag_name, question=que_obj)
                db.session.add(tag_obj)
        db.session.commit()
        return que_obj


class WriteAnswerForm(FlaskForm):
    """回到表单"""
    content = CKEditorField(label='回答内容', validators=[
        DataRequired('回答不能为空'),
        Length(min=5, message='回答内容至少5个字')
    ])

    def save(self, question):
        """保存表单数据"""
        content = self.content.data
        # print(content)
        user = current_user
        answer_obj = Answer(content=content, user=user, question=question)
        db.session.add(answer_obj)
        db.session.commit()
        return answer_obj
