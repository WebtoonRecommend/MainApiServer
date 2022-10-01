from flask import request
from flask_restx import Resource, Api, Namespace
import models
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image # 이미지를 다루는 라이브러리
import pandas as pd
import os

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

WebToon = Namespace('WebToon', description='WebToon DB(웹툰의 정보를 저장하는 DB)와 통신하는 Api')

@WebToon.route('')
class WebToonAdd(Resource):
    @WebToon.doc(params={'file':'이미지 파일, 웹툰의 썸네일을 의미', 'Author':'웹툰의 저자', 'Title':'WebToon의 제목',\
        'Summary':'웹툰의 내용 요약(100자 이내)'})
    def post(self):
        '''Webtoon의 정보를 추가하는 API\n이미지파일, 제목, 요약, 작가를 입력받아 DB에 저장한다.'''
        file = Image.open(request.files['file']) # 파일 열기
        Author = request.form['Author']        
        Title = request.form['Title']
        Summary = request.form['Summary']
        file.save('{}/ApiDir/pictures/'.format(os.getcwd()) + secure_filename(request.files['file'].filename)) # 절대경로로 위치를 지정하여야 저장이 가능함
        ThumbNail = str('{}/ApiDir/pictures/'.format(os.getcwd()) + secure_filename(request.files['file'].filename))
        
        data = models.WebToon(Author=Author, Title=Title, Summary=Summary, ThumbNail=ThumbNail)
        db.session.add(data)
        db.session.commit()
        db.session.flush()

        return 0

@WebToon.route('/<Title>')
class GetWebToonInfo(Resource):
    def get(self, Title):
        '''웹툰의 정보를 가져오는 API\n입력받은 제목과 동일한 웹툰의 정로를 반환한다.'''
        data = models.WebToon.query.filter(models.WebToon.Title.like(Title)).first()
        
        return {
            'Title':data.Title,
            'Author':data.Author,
            'Summary':data.Summary,
            'ThumbNail':data.ThumbNail
        } 