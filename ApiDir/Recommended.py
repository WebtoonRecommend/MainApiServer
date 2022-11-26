from flask_restx import Resource, Api, Namespace, fields
import models
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required

from . import recommend_func

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

Recommended = Namespace('Recommended', description='머신러닝 모델에서 웹툰을 추천받는 API')

# jwt 인증을 위해 헤더를 입력하도록 추가
parser = Recommended.parser()
parser.add_argument('Authorization', location='headers')


@Recommended.route('/<UID>')
class RecommendedGet(Resource):
    @jwt_required() #jwt 검증
    @Recommended.expect(parser)
    def get(self, UID):
        '''
        User에게 웹툰을 추천하는 api\n\
        해당 User의 즐겨찾기와 키워드를 참고하여 추천 목록을 받아온다.\n\
        jwt 인증의 경우 헤더에 Authorization: Bearer jwt를 입력하여야 한다.
        '''

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

            #단어 기반 추천
            # result = recommend_func.FirstRecommendations(keywords)
            # return result

            # 별점 높은 순위
            result = []

            for i in range(len(keywords)):
                temp = db.session.query(models.webtoonInfoJoin).filter(
                    models.webtoonInfoJoin.장르.like("%{}%".format(keywords[i]))
                    ).all()
                temp = [[row.별점, row.이름] for row in temp]
                result.extend(temp)
            
            result = sorted(result, reverse=True) # 별점 순서로 정렬
            
            #중복값 제거
            for i in range(len(result)):
                if i == len(result) - 1:
                    break
                elif result[i][1] == result[i+1][1]:
                    result.pop(i)
            return result[:10]

        else:
            #즐겨찾기 기반 추천
            result = recommend_func.Recommendations10(bookmarks)
            return result