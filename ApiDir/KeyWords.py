from flask import request
from flask_restx import Resource, Api, Namespace
import models
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json

db = SQLAlchemy()

KeyWords = Namespace('KeyWords', description='KeyWords DB(User가 선호하는 키워드를 저장하는 DB)와 통신하는 Api')

@KeyWords.route('', doc={'params':{'UID':'User ID', 'Word':'User가 선택한 키워드'}})
class KeyWordAdd(Resource):
    def post(self):
        '''유저가 회원가입 시 선택한 키워드들을 입력받는 API\n리스트 형태로 전송할 것 ex [{UID:UID, Word:Word}]'''
        data = request.get_json()
        for keyword in data:
            a = models.KeyWords(UID=keyword['UID'], Word=keyword['Word'])
            db.session.add(a)
        db.session.commit()
        db.session.flush()

        return 0

@KeyWords.route('/<UID>')
class KeyWordGet(Resource):
    def get(self, UID):
        '''User가 선택한 키워드들을 리스트 형태로 가져오는 API'''
        data = db.session.query(models.KeyWords).filter(models.KeyWords.UID==UID)
        data = pd.read_sql(data.statement, data.session.bind)
        return json.loads(data.to_json(orient='records'))

@KeyWords.route('/<UID>/<Word>')
class KeyWordDelete(Resource):
    def delete(self, UID, Word):
        '''유저의 ID와 삭제할 키워드를 입력받아 해당하는 row를 삭제하는 API'''
        try:
            db.session.query(models.KeyWords).filter(models.KeyWords.UID==UID, models.KeyWords.Word==Word).delete()
            db.session.commit()
            return 0 # 쿼리 성공 시
        except:
            return 1 # 쿼리 실패 시
