# -*- coding: utf-8 -*-
from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    __tablename__ ='question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    # datetime.now()指的是服务器第一次运行的时间，每次都是同一个
    # datetime.now创建模型的时候获取当前的时间
    create_table=db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('questions'))


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    content=db.Column(db.Text,nullable=False)
    question_id =db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id =db.Column(db.Integer,db.ForeignKey('user.id'))

    question = db.relationship('Question', backref=db.backref('answers',order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))