from flask import request
from flask_restx import Resource, Api, Namespace, fields
import models
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt # 로그인 비밀번호 암호화를 위한 라이브러리
from flask_jwt_extended import *
import config

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

User = Namespace('User', description='User DB(User의 정보를 저장하는 DB)와 통신하는 Api')

#swagger 문서화를 위한 모델 정의
User_field = User.model('User', {
    'ID' : fields.String(description='사용자 ID'),
    'PassWd' : fields.String(description='비밀번호'),
    'Age' : fields.String(description='나이, 숫자로 입력'),
    'Job' : fields.String(description='직업, 숫자로 입력'),
    'Sex' : fields.String(description='나이, 숫자로 입력')
})

parser = User.parser() # 헤더를 추가하기 위한 변수
parser.add_argument('Authorization', location='headers') # 헤더를 입력받기 위해 기대 입력값을 추가

@User.route('') #회원가입의 URL  
class UserAdd(Resource): # user 회원가입
    @User.expect(User_field) # swagger를 통해 데이터베이스를 조작하도록 등록
    def post(self):
        '''User의 정보를 저장하는 API\nId, 비밀번호, 나이, 직업, 성별을 json의 형태로 전달받아 DB에 저장한다.'''

        # 데이터 파싱
        ID = request.json.get('ID')
        PassWd = bcrypt.hashpw(request.json.get('PassWd').encode('utf-8'), bcrypt.gensalt())
        Age = int(request.json.get('Age'))
        Job = int(request.json.get('Job'))
        Sex = int(request.json.get('Sex'))
        print(Age, Job, Sex)

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

    @jwt_required() #jwt 검증
    @User.expect(parser) # 입력값 추가
    def get(self, UID):
        '''User의 정보를 가져오는 API\nID를 입력받아 해당 ID와 동일한 User의 성별, 직업, 나이를 반환한다.\
            jwt 인증의 경우 헤더에 Authorization: Bearer jwt를 입력하여야 한다.'''
        data = db.session.query(models.User).filter(models.User.ID.like(UID)).first()

        return {
            'Age': data.Age,
            'Job': data.Job,
            'Sex': data.Sex
        }
    
    @User.expect(User_field)
    def post(self, UID):
        '''User 로그인 API\n로그인 정보를 받아 옳을 경우 jwt 문자열, 아닐경우 1을 반환한다. id가 존재하지 않는 경우는 2를 반환한다.\
            PassWd만 Json의 형태로 전송하면 된다.'''

        ID = UID
        try:
            data = db.session.query(models.User).filter(models.User.ID.like(ID)).first()
            PW = bcrypt.checkpw(request.json.get('PassWd').encode('utf-8'), data.PassWd) # 비밀번호가 맞는지 확인하는 라이브러리
        except:
            return 2

        if PW == True:
            access_token = create_access_token(identity=UID) #jwt 암호화 및 전송
            return access_token
        else:
           return 1
        