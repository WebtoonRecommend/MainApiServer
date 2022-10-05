from operator import mod
from flask import request
from flask_restx import Resource, Api, Namespace
import models
import pandas as pd
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

Recommended = Namespace('Recommended', description='추천된 웹툰을 저장하는 DB와 통신하는 API')

@Recommended.route('')
class RecommendedAdd(Resource):
    @Recommended.doc(params={'UID':'해당 웹툰을 추천받은 User의 ID', 'Title':'추천받은 웹툰의 제목'})
    def post(self):
        '''User에게 추천할 웹툰을 저장하는 API\n웹툰들을 리스트 형태로 입력받아 저장한다.'''
        data_list = request.get_json()
        for data in data_list:
            a = models.RecommendedList(UID=data['UID'], WebtoonTitle=data['Title'])
            db.session.add(a)
        db.session.commit()
        db.session.flush()

        return 0

@Recommended.route('/<UID>')
class RecommendedGet(Resource):
    
    def get(self, UID):
        '''User가 추천받은 웹툰들을 쿼리하여 가져오는 api\n\
        해당 User의 ID와 동일한 UID를 가진 추천 웹툰들을 리스트 형태로 받아온다.'''
        data = db.session.query(models.RecommendedList).filter(models.RecommendedList.UID==UID)
        data = pd.read_sql(data.statement, data.session.bind)
        return json.loads(data.to_json(orient='records'))