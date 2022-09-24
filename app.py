from flask import Flask
from ApiDir.WorldCup import WorldCup
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

import config

app = Flask(__name__)
api = Api(app)


#orm
db = SQLAlchemy()
migrate = Migrate(app, db) 

# 데이터베이스 초기화
app.config.from_object(config)
db.init_app(app)
migrate.init_app(app, db)
import models

# api 등록
from ApiDir.UserApi import User
from ApiDir.WorldCup import WorldCup
api.add_namespace(User, '/User')
api.add_namespace(WorldCup, '/WorldCup')



if __name__ == '__main__':
    app.run(debug=True)