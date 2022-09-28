from plistlib import UID
from flask import request
from flask_restx import Resource, Api, Namespace
import models
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

BookMark = Namespace('BookMark', description='BookMark DB(User가 선호하는 웹툰를 저장하는 DB)와 통신하는 Api')

@BookMark.route('')
class BookMarkAdd(Resource):
    def post(self):
        '''User가 선호하는 웹툰를 저장하는 API\nUser ID와 웹툰 제목을 json의 형태로 전달받아 DB에 저장한다.'''
        # 데이터 파싱
        UID = request.json.get('UID')
        Title = request.json.get('Title')

        try:
            # BookMark에 맞는 형태로 변환 후 session을 열고 저장
            data = models.BookMark(UID=UID, WebtoonTitle=Title)
            db.session.add(data)
            db.session.commit()
            db.session.flush()
            return 0
        except:
            return 1 # 오류 발생시 코드

@BookMark.route('/<UID>')
class BookMarkList(Resource):
    '''User가 즐겨찾기에 등록한 모든 웹툰들을 쿼리하여 가져오는 api'''
    def get(self, UID):
        data = models.BookMark.query.filter(models.BookMark.UID.like(UID))
        data = pd.read_sql(data)

        return json.loads(data.to_json(orient='records'))
