import json
import pandas as pd

from flask import request
from flask_restx import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity

import models


db = SQLAlchemy()

BookMark = Namespace(
    'BookMark',
    description='BookMark DB(User가 선호하는 웹툰를 저장하는 DB)와 통신하는 Api')

#swagger 문서화를 위한 모델 정의
BookMark_field = BookMark.model(
    'BookMark', 
    {
    'UID' : fields.String(description='사용자 ID'),
    'Title' : fields.String(description='북마크에 저장할 웹툰의 제목')
    }
)

# jwt 헤더를 입력받기 위한 함수
parser = BookMark.parser() 
parser.add_argument('Authorization', location='headers')


@BookMark.route('')
class BookMarkAdd(Resource):
    
    @jwt_required() #jwt 검증
    @BookMark.expect(parser, BookMark_field)
    @BookMark.expect(BookMark_field)
    def post(self):
        '''
        User가 선호하는 웹툰를 저장하는 API\n
        User ID와 웹툰 제목을 json의 형태로 전달받아 DB에 저장한다.\n
        uid는 필요없음'''
        
        # 데이터 파싱
        Title = request.json.get('Title')

        try:
            # BookMark에 맞는 형태로 변환 후 session을 열고 저장
            data = models.BookMark(UID=get_jwt_identity(), WebtoonTitle=Title) # id를 입력 받는 것이 아니라 jwt에서 추출
            db.session.add(data)
            db.session.commit()
            db.session.flush()
            return 0
        except:
            return 1 # 오류 발생시 코드


@BookMark.route('/<UID>')
class BookMarkList(Resource):
    
    @jwt_required() #jwt 검증
    @BookMark.expect(parser)
    def get(self, UID):
        '''
        User가 즐겨찾기에 등록한 모든 웹툰들을 쿼리하여 가져오는 api\n\
        해당 User의 ID와 동일한 UID를 가진 모든 북마크들을 리스트 형태로 받아온다.\n
        만약 jwt의 주인의 id와 가져올 데이터의 id가 다른 경우 1을 반환한다.'''

        temp_id = get_jwt_identity()
        if temp_id == UID:
            data = db.session.query(models.BookMark).filter(models.BookMark.UID==UID)
            data = pd.read_sql(data.statement, data.session.bind)
            return json.loads(data.to_json(orient='records'))
        else:
            return 1 # 요청한 id와 가져올 데이터의 id가 다른 경우


@BookMark.route('/<UID>/<WebToonTitle>')
class BookMarkDelete(Resource):

    @jwt_required() #jwt 검증
    @BookMark.expect(parser)
    def delete(self, UID, WebToonTitle):
        '''
        User가 즐겨찾기에 등록한 웹툰 삭제\n\
        BookMark DB의 값 중에서 UID와 WebToonTitle이 동일한 항목 삭제
        '''
        
        # jwt로 부터 id 추출
        temp_id = get_jwt_identity()

        # 데이터를 요청한 jwt와 반환할 데이터의 uid가 일치하는지 확인 및 데이터 반환
        if temp_id == UID:
            try:
                db.session.query(models.BookMark).filter(models.BookMark.UID==UID, models.BookMark.WebtoonTitle==WebToonTitle).delete()
                db.session.commit()
                return 0 # 쿼리 성공 시
            except:
                return 1 # 쿼리 실패 시
        else:
            return "jwt와 가져올 데이터의 id가 일치하지 않습니다."
        
