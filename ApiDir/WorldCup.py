import json
from sqlite3 import Cursor
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import models
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출


WorldCup = Namespace('WorldCup', description='WorldCup DB(이상형 월드컵의 정보를 저장하는 DB)와 통신하는 Api')

@WorldCup.route('')
class WorldCupAdd(Resource): # worldcup log 기록
    def post(self):
        '''월드컵 결과를 저장하는 API\n json의 형태로 데이터를 전달받으며, 웹툰의 제목, 해당 웹툰이 최종으로 진출한 라운드, 월드컵을 진행한 User의 Id가 필요하다.'''
        # 데이터 파싱
        WebtoonTitle = request.json.get('WebtoonTitle')
        Round = int(request.json.get('Round'))
        UID = request.json.get('UID')

        try:
            # worldcup에 맞는 형태로 변환 후 session을 열고 저장
            WCDATA = models.WorldCup(Round=Round, UID=UID, WebtoonTitle=WebtoonTitle)
            db.session.add(WCDATA)
            db.session.commit()
            db.session.flush()
            return 0
        except:
            return 1 # 오류 발생시 코드

@WorldCup.route('/<UID>')
class WorldCupFind(Resource):
    def get(self, UID):
        '''월드컵 결과를 가져오는 API\n UID와 동일한 UID를 가진 row를 모두 찾아 반환한다.'''
        # pandas를 이용해 sql문을 해석한 후 json으로 변환 https://lemontia.tistory.com/844
        
        UIDWCDATA = models.WorldCup.query.filter(models.WorldCup.UID.like(UID))
        
        UIDWCDATA = pd.read_sql(UIDWCDATA.statement, UIDWCDATA.session.bind) 
        
        return json.loads(UIDWCDATA.to_json(orient='records'))
