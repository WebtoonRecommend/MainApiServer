from flask import Flask
from ApiDir.BookMark import BookMark
from ApiDir.WebToon import WebToon
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import *

import config

app = Flask(__name__)
CORS(app, resources={r'*':{'origins':'*'}})
api = Api(app, title='DB Server Api', description='데이터베이스와 통신하기 위한 서버입니다.\n User, WorldCup, WebToob Table이 존재합니다. \
    \n 로그인 이후에는 기능을 사용하기 위해 jwt 토큰을 헤더를 통해 전송해야합니다.')

#auth
app.config['JWT_SECRET_KEY'] = 'WebTune'
jwt = JWTManager(app)

#orm
db = SQLAlchemy()


# 데이터베이스 초기화
app.config.from_object(config)
db.init_app(app)

import models

# api 등록
from ApiDir.UserApi import User
from ApiDir.WebToon import WebToon
from ApiDir.BookMark import BookMark
from ApiDir.Recommended import Recommended
from ApiDir.KeyWords import KeyWords
api.add_namespace(User, '/User')
api.add_namespace(WebToon, '/WebToon')
api.add_namespace(BookMark, '/BookMark')
api.add_namespace(Recommended, '/Recommended')
api.add_namespace(KeyWords, '/KeyWords')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)