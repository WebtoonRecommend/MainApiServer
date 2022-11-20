from flask_restx import Resource, Api, Namespace, fields
#import models
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import *
from . import recommend_func

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

Recommended = Namespace('Recommended', description='머신러닝 모델에서 웹툰을 추천받는 API')

parser = Recommended.parser()
parser.add_argument('Authorization', location='headers')

# @Recommended.route('')
# class RecommendedAdd(Resource):
#     @Recommended.doc(params={'UID':'해당 웹툰을 추천받은 User의 ID', 'Title':'추천받은 웹툰의 제목'})
#     @jwt_required() #jwt 검증
#     def post(self):
#         '''User에게 추천할 웹툰을 저장하는 API\n웹툰들을 리스트 형태로 입력받아 저장한다.'''
#         data_list = request.get_json()
#         for data in data_list:
#             a = models.RecommendedList(UID=data['UID'], WebtoonTitle=data['Title'])
#             db.session.add(a)
#         db.session.commit()
#         db.session.flush()

#         return 0

@Recommended.route('/<UID>')
class RecommendedGet(Resource):
    @jwt_required() #jwt 검증
    @Recommended.expect(parser)
    def get(self, UID):
        '''User에게 웹툰을 추천하는 api\n\
        해당 User의 즐겨찾기와 키워드를 참고하여 추천 목록을 받아온다.\n\
        jwt 인증의 경우 헤더에 Authorization: Bearer jwt를 입력하여야 한다.'''
        
        # 즐겨찾기 목록 가져오기

        # 쿼리 결과의 형태를 읽을 수 있는 형태로 변환(.fetchall의 역할)
        bookmarks = db.session.execute("select WebtoonTitle from book_mark where UID='{}'".format(UID)).fetchall() 

        bookmarks = [row[0] for row in bookmarks] # 리스트 형태로 변환
        print(bookmarks)

        # 즐겨찾기 목록을 먼저 확인한 후 해당 유저가 즐겨찾기를 추가하지 않았으면 키워드를 확인한다.

        if len(bookmarks) == 0:
            keywords = db.session.execute("select Word from key_words where UID='{}'".format(UID)).fetchall()
            keywords = [row[0] for row in keywords]
            result = recommend_func.FirstRecommendations(keywords) # 추천 함수 호출
            return result
        else:
            result = recommend_func.Recommendations10(bookmarks) # 추천 함수 호출
            return result


    # def delete(self, UID, methods=['DELETE']):
    #     '''UID를 입력받아 UID가 일치하는 모든 추천 웹툰들을 삭제하는 API'''

    #     try:
    #         delete_list = db.session.query(models.RecommendedList).filter(models.RecommendedList.UID==UID).all()
    #         for i in delete_list:
    #             db.session.delete(i)
    #         db.session.commit()
    #         return 0 # 쿼리 성공 시
    #     except:
    #         return 1 # 쿼리 실패 시

# @Recommended.route('/<UID>/<Title>')
# class RecommendedDelete(Resource):
#     @jwt_required() #jwt 검증
#     def delete(self, UID, Title):
#         '''User의 추천 목록 리스트에서 제목과 UID가 일치하는 웹툰을 삭제하는 API'''

#         try:
#             db.session.query(models.RecommendedList).filter(models.RecommendedList.UID==UID, models.RecommendedList.WebtoonTitle==Title).delete()
#             db.session.commit()
#             return 0 # 쿼리 성공 시
#         except:
#             return 1 # 쿼리 실패 시