#파일 전송 테스트 파일

import requests

img = open('horse.png', 'rb') #전송할 사진을 MainApiServer 에 넣고 사용

files = {
    'file': img
}

data = {
    "Author": "0000000000",
    "Title": "1234567890",
    "Summary" : "00000000000",
}

res = requests.post('https://127.0.0.1:5000/WebToon', files=files, data=data)