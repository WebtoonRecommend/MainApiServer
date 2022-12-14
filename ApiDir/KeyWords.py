import pandas as pd
import json

from flask import request
from flask_restx import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity

import models


db = SQLAlchemy()

KeyWords = Namespace(
    "KeyWords", description="KeyWords DB(User가 선호하는 키워드를 저장하는 DB)와 통신하는 Api"
)

parser = KeyWords.parser()  # 헤더를 추가하기 위한 변수
parser.add_argument("Authorization", location="headers")

# swagger 문서화를 위한 모델 정의
KeyWord_field = KeyWords.model(
    "KeyWords",
    {
        "Word": fields.String(description="사용자가 선호하는 단어"),
    },
)


@KeyWords.route("")
class KeyWordAddGet(Resource):
    @jwt_required()  # jwt 검증
    @KeyWords.expect(parser)  # 검증용 헤더 추가
    def get(self):
        """User가 선택한 키워드들을 리스트 형태로 가져오는 API"""

        UID = get_jwt_identity()
        data = db.session.query(models.KeyWords).filter(models.KeyWords.UID == UID)
        data = pd.read_sql(data.statement, data.session.bind)
        if len(data) == 0:
            return "You don't add any Keyword. Please add Keyword."
        else:
            return json.loads(data.to_json(orient="records"))

    @jwt_required()  # jwt 검증
    @KeyWords.expect(parser, KeyWord_field)  # 검증용 헤더 추가
    def post(self):
        """유저가 회원가입 시 선택한 키워드들을 입력받는 API\n
        리스트 형태로 전송할 것 ex) [{Word:Word}]
        """

        data = request.get_json()
        for keyword in data:
            a = models.KeyWords(UID=get_jwt_identity(), Word=keyword["Word"])
            db.session.add(a)
        db.session.commit()
        db.session.flush()

        return 0


@KeyWords.route("/<Word>")
class KeyWordDelete(Resource):
    @jwt_required()  # jwt 검증
    @KeyWords.expect(parser)  # 검증용 헤더 추가
    def delete(self, Word):
        """유저의 ID와 삭제할 키워드를 입력받아 해당하는 row를 삭제하는 API"""
        UID = get_jwt_identity()
        try:
            db.session.query(models.KeyWords).filter(
                models.KeyWords.UID == UID, models.KeyWords.Word == Word
            ).delete()
            db.session.commit()
            return 0  # 쿼리 성공 시
        except:
            return 1  # 쿼리 실패 시
