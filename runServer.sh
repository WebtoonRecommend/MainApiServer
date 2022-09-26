#도커 파일이 위치한 디렉토리에서 실행하세요.

#도커 빌드 및 실행
sudo docker build -t apiserver:0.0 .
sudo docker run -it -p 80:5000 -v $(pwd):/home apiserver:0.0
