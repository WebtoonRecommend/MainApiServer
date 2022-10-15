from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

class User(db.Model):
    ID = db.Column(db.String(10), primary_key=True)
    PassWd = db.Column(db.String(100))
    Age = db.Column(db.Integer)
    Job = db.Column(db.Integer) # 직업의 유형별로 분류하여 숫자로 인코딩 할 예정
    Sex = db.Column(db.Integer)

class WebToon(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key = True) # 자동으로 기본키 생성(autoincrement)
    Author = db.Column(db.String(10))
    Title = db.Column(db.String(10), nullable=False)
    Summary = db.Column(db.String(100))
    ThumbNail = db.Column(db.String(100))

class WorldCup(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Round = db.Column(db.Integer)
    UID = db.Column(db.String(10))
    WebtoonTitle = db.Column(db.String(10))

class BookMark(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UID = db.Column(db.String(10))
    WebtoonTitle = db.Column(db.String(10))

class RecommendedList(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UID = db.Column(db.String(10))
    WebtoonTitle = db.Column(db.String(10))

class KeyWords(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    UID = db.Column(db.String(10))
    Word = db.Column(db.String(10))

class webtoonInfoJoin(db.Model):
    __bind_key__ = 'test'
    웹툰ID = db.Column(db.Text, primary_key=True)
    이름 = db.Column(db.Text)
    작가 = db.Column(db.Text)
    설명 = db.Column(db.Text)
    장르 = db.Column(db.Text)
    이용가 = db.Column(db.Text)
    회차 = db.Column(db.Text)
    별점 = db.Column(db.Text)
    완결 = db.Column(db.Text)
    플랫폼 = db.Column(db.Text)
    링크 = db.Column(db.Text)
    이미지링크 = db.Column(db.Text)
    썸네일 = db.Column(db.Text)