from flask_restx import Resource, Api, Namespace, fields
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity

import models
from . import recommend_func

db = SQLAlchemy()  # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

Recommended = Namespace("Recommended", description="머신러닝 모델에서 웹툰을 추천받는 API")

# jwt 인증을 위해 헤더를 입력하도록 추가
parser = Recommended.parser()
parser.add_argument("Authorization", location="headers")


@Recommended.route("/<days>")
class RecommendedGet(Resource):
    @jwt_required()  # jwt 검증
    @Recommended.expect(parser)
    def get(self, days):
        """User에게 웹툰을 추천하는 api\n\
        해당 User의 즐겨찾기와 키워드를 참고하여 추천 목록을 받아온다.\n\
        jwt 인증의 경우 헤더에 Authorization: Bearer jwt를 입력하여야 한다.
        """

        UID = get_jwt_identity()
        # 즐겨찾기 목록 가져오기
        # 쿼리 결과의 형태를 읽을 수 있는 형태로 변환(.fetchall의 역할)
        bookmarks = db.session.execute(
            "select WebtoonTitle from book_mark where UID='{}'".format(UID)
        ).fetchall()
        bookmarks = [row[0] for row in bookmarks]

        # 즐겨찾기 목록을 먼저 확인한 후 해당 유저가 즐겨찾기를 추가하지 않았으면 키워드를 확인한다.
        if len(bookmarks) == 0:
            keywords = db.session.execute(
                "select Word from key_words where UID='{}'".format(UID)
            ).fetchall()
            keywords = [row[0] for row in keywords]

            # 단어 기반 추천
            try:
                result = recommend_func.FirstRecommendations(keywords, int(days))

                # 평점 순서대로 정렬
                for i in result:
                    i[0] = float(
                        db.session.query(models.webtoonInfoJoin)
                        .filter(models.webtoonInfoJoin.이름 == i[1])
                        .first()
                        .별점
                    )
                print(result)
                result = sorted(result, reverse=True)
            except ValueError:
                return "Please enter a 'Only Number' for days"
            except ZeroDivisionError:
                return "This User doesn't add KeyWord"

            return result

        else:
            # 즐겨찾기 기반 추천
            try:
                result = recommend_func.Recommendations10(bookmarks, int(days))

                # 평점 순서대로 정렬
                for i in result:
                    i[0] = float(
                        db.session.query(models.webtoonInfoJoin)
                        .filter(models.webtoonInfoJoin.이름 == i[1])
                        .first()
                        .별점
                    )
                print(result)
                result = sorted(result, reverse=True)
            except ValueError:
                return "Please enter a 'Only Number' for days"
            return result
