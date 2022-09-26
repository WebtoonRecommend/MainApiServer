#파일 전송 테스트 파일

import requests

img = open('horse.png', 'rb')

files = {
    'file': img
}

data = {
    "Author": "0000000000",
    "Title": "1234567890",
    "Summary" : "00000000000",
}

res = requests.post(' http://127.0.0.1:5000/WebToon', files=files, data=data)