# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session
import config
from models import User, Question, Answer
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
app.debug = True

#
# RuntimeError: application not registered on db instance and no application bound to current context
# sove this problem
db.init_app(app)


@app.route('/')
def index():
    # 按照时间比较大的排在前面,在create_time前面加(-)
    context = {
        'questions':Question.query.order_by('-create_table').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone , User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果在31天内都不需要登录
            session.permanent = True
            # return redirect(url_for('index'))
            print(session.get("user_id"))
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后重新登录'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 手机号码，如果被注册了，不能注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已经被注册,请更换手机号码'
        else:
            user = User(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    # 清除session数据
    session.clear()
    return redirect(url_for('login'))


@app.route('/question/',methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model=Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))

 #这个上下文处理器(装饰器)修饰的钩子函数，必须返回一个字典，即使为{空字典}
 #上下文处理器中返回的字典，'key'值会在模板中当成变量被渲染
 #上下文处理器返回的字典，在所有页面中都是可用的
 #
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        print(user.username)
        if user:
            return {'user':user}
    # return {'username':'test'}
    return {}





