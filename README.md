# MainApiServer
어플리케이션과 통신할 api서버입니다

# 서버 실행 방법
## 1. docker를 설치합니다


## 2. recommended_learning 레포지토리와 크롤링 레포지토리를 다운받고 실행합니다.
실행후 생성된 파일을 MainApiServer 디렉토리로 옮깁니다.



## 3. flask 실행
우분투 환경의 경우 MainApiServer 디렉토리에서 
. runServer.sh
명령어를 실행합니다.


# 버전 관리
버전 관리의 경우 flask migration을 사용합니다. 버전 관리에 사용되는 디렉토리는 ServerMange입니다.


# 코드 설명



## ApiDir 폴더
해당 폴더는 서버의 Api가 저장되어 있는 폴더입니다.



## 기타 파일



### ~~~Test.py 파일들은 api 파일을 통해 생성된 api 함수가 오류가 없는지 검증하는 파일입니다.



### Api.db와 test.db는 제공되지 않습니다. 직접 크롤링 서버를 실행시키십시요.