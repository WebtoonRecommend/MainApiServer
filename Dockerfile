FROM ubuntu:20.04
RUN apt-get update; apt-get install -y python3-pip; \
    pip install virtualenv; mkdir myproject; virtualenv venv; . venv/bin/activate; \
    pip install Flask==2.1.2; pip install flask-restx; pip install werkzeug==2.1.2; pip install sqlalchemy; pip install Flask-Migrate; \
    pip install pandas; pip install pillow; pip install flask-bcrypt==1.0.0


CMD cd /; . /venv/bin/activate;\
    cd /; cd home;\
    python3 app.py