from flask import request
from flask_restx import Resource, Api, Namespace, fields
import models
from flask_sqlalchemy import SQLAlchemy
#from PIL import Image # 이미지를 다루는 라이브러리
import pandas as pd
import json
from flask_jwt_extended import *

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

WebToon = Namespace('WebToon', description='WebToon DB(웹툰의 정보를 저장하는 DB)와 통신하는 Api')

#swagger 문서화를 위한 모델 정의
WebToon_field = WebToon.model('WebToon', { # 아직 안함
    'ID' : fields.String(description='사용자 ID'),
    'PassWd' : fields.String(description='비밀번호'),
    'Age' : fields.String(description='나이, 숫자로 입력'),
    'Job' : fields.String(description='직업, 숫자로 입력'),
    'Sex' : fields.String(description='나이, 숫자로 입력')
})

@WebToon.route('')
class WebToonAdd(Resource):
    @WebToon.doc(params={'ThumbNail':'썸네일이 저장된 링크', 'Author':'웹툰의 저자', 'Title':'WebToon의 제목',\
        'Summary':'웹툰의 내용 요약(100자 이내)'})
    @jwt_required() #jwt 검증
    def post(self):
        '''Webtoon의 정보를 추가하는 API\n이미지 링크, 제목, 요약, 작가를 입력받아 DB에 저장한다.'''
        #file = Image.open(request.files['file']) # 파일 열기
        Author = request.json.get('Author')        
        Title = request.json.get('Title')
        Summary = request.json.get('Summary')
        #file.save('{}/ApiDir/pictures/'.format(os.getcwd()) + secure_filename(request.files['file'].filename)) # 절대경로로 위치를 지정하여야 저장이 가능함
        ThumbNail = request.json.get('ThumbNail')#str('{}/ApiDir/pictures/'.format(os.getcwd()) + secure_filename(request.files['file'].filename))
        
        data = models.WebToon(Author=Author, Title=Title, Summary=Summary, ThumbNail=ThumbNail)
        db.session.add(data)
        db.session.commit()
        db.session.flush()

        return 0

@WebToon.route('/<Title>')
class WebToonInfo(Resource):

    parser = WebToon.parser() # 헤더를 추가하기 위한 변수
    parser.add_argument('Authorization', location='headers') # 헤더를 입력받기 위해 기대 입력값을 추가

    @jwt_required() #jwt 검증
    @WebToon.expect(parser)
    def get(self, Title):
        '''웹툰의 정보를 가져오는 API\n입력받은 제목과 동일한 웹툰의 정보를 반환한다.'''
        data = models.webtoonInfoJoin.query.filter(models.webtoonInfoJoin.이름.like(Title)).first()
        
        return {
            '이름':data.이름,
            '작가':data.작가,
            '설명':data.설명,
            '장르':data.장르,
            '이용가':data.이용가,
            '회차':data.회차,
            '완결':data.완결,
            '플랫폼':data.플랫폼,
            '링크':data.링크,
            '이미지링크':data.이미지링크,
            '별점':data.별점,
            '썸네일':data.썸네일,
        }         
    
    @jwt_required() #jwt 검증
    def delete(self, Title):
        '''웹툰의 제목을 입력받아 해당하는 웹툰을 삭제하는 API'''
        try:
            db.session.query(models.webtoonInfoJoin).filter(models.webtoonInfoJoin.이름==Title).delete()
            db.session.commit()
            return 0 # 쿼리 성공 시
        except:
            return 1 # 쿼리 실패 시

@WebToon.route('/Search/<Title>')
class SearchWebToon(Resource):
    parser = WebToon.parser() # 헤더를 추가하기 위한 변수
    parser.add_argument('Authorization', location='headers') # 헤더를 입력받기 위해 기대 입력값을 추가

    @jwt_required() #jwt 검증
    @WebToon.expect(parser)
    def get(self, Title):
        '''웹툰의 정보를 검색하는 api'''
        import sqlite3
        con = sqlite3.connect('./test.db')
        data = pd.read_sql("SELECT * FROM webtoon_info_join WHERE 이름 like '%{}%'".format(Title), con)
        return json.loads(data.to_json(orient='records'))