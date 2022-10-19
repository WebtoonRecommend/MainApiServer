from flask import request
from flask_restx import Resource, Api, Namespace
import models
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt # 로그인 비밀번호 암호화를 위한 라이브러리

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

User = Namespace('User', description='User DB(User의 정보를 저장하는 DB)와 통신하는 Api')

@User.route('', doc={'params':{'ID':'User가 입력한 ID(10자 이내)', 'PassWd':'User가 입력한 PassWd(10자 이내)',\
     'Age':'User의 나이(숫자가 아닌 문자열)','Job':'유저의 직업(분류별로 int형태로 나타내지만 문자열)', 'Sex':'0 혹은 1로 나타내지만 문자열'}}) # 입력 parameter swagger 추가     
class UserAdd(Resource): # user 회원가입
    
    def post(self):
        '''User의 정보를 저장하는 API\nId, 비밀번호, 나이, 직업, 성별을 json의 형태로 전달받아 DB에 저장한다.'''
        # 데이터 파싱
        ID = request.json.get('ID')
        PassWd = bcrypt.hashpw(request.json.get('PassWd').encode('utf-8'), bcrypt.gensalt())
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
        '''User의 정보를 가져오는 API\nID를 입력받아 해당 ID와 동일한 User의 성별, 직업, 나이를 반환한다.'''
        data = db.session.query(models.User).filter(models.User.ID.like(UID)).first()

        return {
            'Age': data.Age,
            'Job': data.Job,
            'Sex': data.Sex
        }
    
    @User.doc(params={'PassWd':'로그인할 유저가 입력한 비밀번호'})
    def post(self, UID):
        '''User 로그인 API\n로그인 정보를 받아 옳을 경우 0 아닐경우 1을 반환한다. id가 존재하지 않는 경우는 2를 반환한다.'''

        ID = UID
        try:
            data = db.session.query(models.User).filter(models.User.ID.like(ID)).first()
            PW = bcrypt.checkpw(request.json.get('PassWd').encode('utf-8'), data.PassWd) # 비밀번호가 맞는지 확인하는 라이브러리
        except:
            return 2

        if PW == True:
            return 0
        else:
           return 1
        