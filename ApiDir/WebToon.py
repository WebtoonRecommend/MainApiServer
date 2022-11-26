import pandas as pd
import json
import sqlite3

from flask import request
from flask_restx import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required

import models


db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

WebToon = Namespace(
    'WebToon',
    description='WebToon DB(웹툰의 정보를 저장하는 DB)와 통신하는 Api')

parser = WebToon.parser() # 헤더를 추가하기 위한 변수
parser.add_argument('Authorization', location='headers') # 헤더를 입력받기 위해 기대 입력값을 추가


@WebToon.route('/<Title>')
class WebToonInfo(Resource):

    @jwt_required() #jwt 검증
    @WebToon.expect(parser)
    def get(self, Title):
        '''웹툰의 정보를 가져오는 API\n
        입력받은 제목과 동일한 웹툰의 정보를 반환한다.
        '''

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
    

@WebToon.route('/Search/<Title>')
class SearchWebToon(Resource):

    @jwt_required() #jwt 검증
    @WebToon.expect(parser)
    def get(self, Title):
        '''웹툰의 정보를 검색하는 api'''
        
        con = sqlite3.connect('./test.db')
        data = pd.read_sql(
            "SELECT * FROM webtoon_info_join WHERE 이름 like '%{}%'".format(Title), con)

        return json.loads(data.to_json(orient='records'))