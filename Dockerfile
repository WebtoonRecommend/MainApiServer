FROM ubuntu:20.04
RUN apt-get update; apt-get install -y python3-pip; \
    pip install virtualenv; mkdir myproject; virtualenv venv; . venv/bin/activate; \
    pip install Flask==2.0.2; pip install flask-restx==0.5.1; pip install werkzeug==2.0.2; pip install sqlalchemy==1.3.23; pip install Flask-Migrate; \
    pip install pandas==1.5.0; pip install pillow==9.2.0; pip install flask-bcrypt==1.0.1


CMD cd /; . /venv/bin/activate;\
    cd /; cd home;\
    python3 app.py