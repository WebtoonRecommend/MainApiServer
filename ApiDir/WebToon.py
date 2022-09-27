from flask import request
from flask_restx import Resource, Api, Namespace
import models
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image # 이미지를 다루는 라이브러리
import pandas as pd
import os
import json

db = SQLAlchemy() # app.py에서 sqlalchemy 호출시 순환 호출 오류 발생하여 각 api마다 호출

WebToon = Namespace('WebToon')

@WebToon.route('')
class WebToonAdd(Resource):
    def post(self):
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
        data = models.WebToon.query.filter(models.WebToon.Title.like(Title)).first()
        
        return {
            'Title':data.Title,
            'Author':data.Author,
            'Summary':data.Summary,
            'ThumbNail':data.ThumbNail
        } 