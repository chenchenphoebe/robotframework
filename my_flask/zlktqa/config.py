# -*- coding: utf-8 -*-
import os

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'MockServer'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_TRACK_MODIFICATIONS = False