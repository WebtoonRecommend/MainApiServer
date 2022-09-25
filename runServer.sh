#도커 파일이 위치한 디렉토리에서 실행하세요.

sudo docker build -t apiserver:0.0 .
sudo docker run -it -v --name -p $(pwd) server 5000:5000 apiserver:0.0
