from ApiDir import db

class User(db.Model):
    ID = db.Column(db.String(10), primary_key=True)
    PassWd = db.Column(db.String(10))
    Age = db.Column(db.Integer)
    Job = db.Column(db.Integer) # 직업의 유형별로 분류하여 숫자로 인코딩 할 예정
    Sex = db.Column(db.Integer)

class WebToon(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key = True) # 자동으로 기본키 생성(autoincrement)
    Author = db.Column(db.String(10))
    Title = db.Column(db.String(10), nullable=False)
    Summary = db.Column(db.String(100))
    ThumbNail = db.Column(db.String(20))

class WorldCup(db.Model):
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Round = db.Column(db.Integer)
    UID = db.Column(db.String(10))
    WebtoonTitle = db.Column(db.String(10))

