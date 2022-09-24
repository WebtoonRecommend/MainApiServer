FROM ubuntu:20.04
RUN sudo apt-get update; apt-get install -y python-pip; \
    pip install virtualenv; mkdir myproject; virtualenv venv; . venv/bin/activate; \
    pip install Flask; pip install flask-restx; pip install sqlalchemy; pip install Flask-Migrate