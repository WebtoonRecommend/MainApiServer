from flask import request
from flask_restx import Resource, Api, Namespace
from ApiDir import db
import models

User = Namespace('User')

@User.route('')
class UserAdd(Resource): # user 회원가입
    def post(self):
        # 데이터 파싱
        ID = request.json.get('ID')
        PassWd = request.json.get('PassWd')
        Age = int(request.json.get('Age'))
        Job = int(request.json.get('Job'))
        Sex = int(request.json.get('Sex'))

        try:
            # user에 맞는 형태로 변환 후 session을 열고 저장
            User_data = models.User(ID=ID, PassWd=PassWd, Age=Age, Job=Job, Sex=Sex)
            db.session.add(User_data)
            db.session.commit()
            db.session.flush()
            return 0
        except:
            return 1 # 오류 발생시 코드

@User.route('/<UID>')
class UserEdit(Resource):
    def get(self, UID):
        UserId = str(UID)
        data = db.session.query(models.User).filter(models.User.ID.like(UID)).first()

        return {
            'Age': data.Age,
            'Job': data.Job,
            'Sex': data.Sex
        }