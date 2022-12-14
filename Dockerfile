FROM ubuntu:20.04
RUN apt-get update; apt-get install -y python3-pip; \
    pip install virtualenv; mkdir myproject; virtualenv venv; . venv/bin/activate; \
    pip install Flask==2.1.2; pip install flask-restx; pip install werkzeug==2.1.2; pip install sqlalchemy; pip install -U Flask-SQLAlchemy==2.5.1; \
    pip install pandas; pip install pillow; pip install Flask-Bcrypt==1.0.1; pip install Flask==2.1.2; pip install flask-restx; pip install werkzeug==2.1.2; \
    pip install flask_cors; pip install flask-jwt-extended; pip install gensim; pip install gunicorn


CMD cd /; . /venv/bin/activate;\
    cd /; cd home;\
    gunicorn -b 0.0.0.0:5001 app:app