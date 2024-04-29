from flask import Blueprint, render_template, request, abort, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from models import Question, Answer, AnswerComment, db
from qa.form import WriteQuestionForm, WriteAnswerForm

qa = Blueprint('qa', __name__,
               template_folder='templates',
               static_folder='../assets')


@qa.route('/')
def index():
    """ 首页 - 回答列表 """
    per_page = 3  # 每页数据的大小
    page = int(request.args.get('page', 1))
    data_list = Answer.query.filter_by(is_valid=1)
    page_data = data_list.paginate(page=page, per_page=per_page)
    return render_template('index.html', page_data=page_data)


@qa.route('/follow')
def follow():
    """ 关注 - 问题列表 """
    per_page = 20  # 每页数据的大小
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=1).paginate(
        page=page, per_page=per_page)
    return render_template('follow.html', page_data=page_data)


@qa.route('/qa/list')
def question_list():
    """查询问题数据列表
    // json
    {
        'code': 0
        'data': ''
    }
    """
    try:
        per_page = 2  # 每页数据的大小
        page = int(request.args.get('page', 1))
        qa_list = Question.query.filter_by(is_valid=True)
        page_data = qa_list.paginate(page=page, per_page=per_page)
        data = render_template('qa_list.html', page_data=page_data)
        return {'code': 0, 'data': data}
    except Exception as e:
        print(e)
        data = ''
    return {'code': 1, 'data': data}
    # return render_template('qa_list.html', page_data=page_data)


@qa.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    """ 写文章，提问 """
    form = WriteQuestionForm()
    if form.validate_on_submit():
        try:
            que_obj = form.save()
            if que_obj:
                flash('发布问题成功', 'success')
                return redirect(url_for('qa.index'))
        except Exception as e:
            print(e)
        flash('发布问题失败，请稍后重试', 'danger')
    return render_template('write.html', form=form)


@qa.route('/detail/<int:q_id>', methods=['GET', 'POST'])
def detail(q_id):
    """ 问题详情 """
    # 1. 查询问题信息
    question = Question.query.get(q_id)
    if not question.is_valid:
        abort(404)
    # 2. 展示第一条回答信息
    answer = question.answer_list.filter_by(is_valid=True).first()
    # 添加回答
    form = WriteAnswerForm()
    if form.validate_on_submit():
        try:
            if not current_user.is_authenticated:
                flash('请先登录', 'danger')
                return redirect(url_for('accounts.login'))
            form.save(question=question)
            flash('回答问题成功', 'success')
            redirect(url_for('qa.detail', q_id=q_id))
        except Exception as e:
            print(form.errors)
            print(e)
    return render_template('detail.html',
                           question=question,
                           answer=answer,
                           form=form
                           )


@qa.route('/comments/<int:answer_id>', methods=['GET', 'POST'])
def comments(answer_id):
    """评论"""
    answer = Answer.query.get(answer_id)
    if request.method == 'POST':
        # 添加评论
        try:
            if not current_user.is_authenticated:
                result = {'code': 1, 'message': '请登录'}
                return jsonify(result), 400
            # 1、获取数据
            content = request.form.get('content', '')
            reply_id = request.form.get('reply_id', None)
            question = answer.question
            # 2、保存到数据库
            comment_obj = AnswerComment(
                content=content,
                reply_id=reply_id,
                user=current_user,
                answer=answer,
                question=question
            )
            db.session.add(comment_obj)
            db.session.commit()
            return '', 201
        except Exception as e:
            print(e)
            result = {'code': 1, 'message': '服务器正忙，请稍后重试'}
            return jsonify(result), 400
    else:
        # 获取评论列表
        try:
            page = int(request.args.get('page', 1))
            per_page = 2
            data_list = answer.comment_list()
            page_data = data_list.paginate(page=page, per_page=per_page)
            data = render_template('comments.html', page_data=page_data, answer=answer)
            result = {'code': 0, 'data': data, 'meta': {'page': page}}
            return jsonify(result), 200
        except Exception as e:
            print(e)
            result = {'code': 1, 'data': '', 'message': '服务器正忙'}
            return jsonify(result), 500


@qa.route('/comment/love/<int:comment_id>', methods=['POST'])
def comment_love(comment_id):
    """评论点赞"""
    try:
        # ******* 使用异步接口调用，不适合用login_required判断用户登录状态 ********
        if not current_user.is_authenticated:
            return '',401
        comment_obj = AnswerComment.query.get(comment_id)
        comment_obj.love_count += 1
        db.session.add(comment_obj)
        db.session.commit()
    except Exception as e:
        print(e)
        # abort(500)
        return '', 500
    return '', 201

