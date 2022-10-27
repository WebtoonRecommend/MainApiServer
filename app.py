from re import T
from flask import Flask
from ApiDir.BookMark import BookMark
from ApiDir.WebToon import WebToon
from ApiDir.WorldCup import WorldCup
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import config

app = Flask(__name__)
CORS(app, resources={r'*':{'origins':'*'}})
api = Api(app, title='DB Server Api', description='데이터베이스와 통신하기 위한 서버입니다.\n User, WorldCup, WebToob DB가 존재합니다.')


#orm
db = SQLAlchemy()


# 데이터베이스 초기화
app.config.from_object(config)
db.init_app(app)

import models

# api 등록
from ApiDir.UserApi import User
from ApiDir.WorldCup import WorldCup
from ApiDir.WebToon import WebToon
from ApiDir.BookMark import BookMark
from ApiDir.Recommended import Recommended
from ApiDir.KeyWords import KeyWords
api.add_namespace(User, '/User')
api.add_namespace(WorldCup, '/WorldCup')
api.add_namespace(WebToon, '/WebToon')
api.add_namespace(BookMark, '/BookMark')
api.add_namespace(Recommended, '/Recommended')
api.add_namespace(KeyWords, '/KeyWords')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)