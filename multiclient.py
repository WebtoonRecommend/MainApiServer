import requests
from time import sleep

img0 = open('horse0.png', 'rb') #전송할 사진을 MainApiServer 에 넣고 사용
img1 = open('horse1.png', 'rb')
img2 = open('horse2.png', 'rb')
files = [
    {
        'file': img0
    },
    {
        'file': img1
    },
    {
        'file': img1
    },

]
#res = requests.post('http://3.39.22.234/WebToon', files=files, data=data, verify=False)


# 테스트를 위한 웹툰 대량생성 함수
data_list = [
  {
    "Author": "cu",
    "Title": "신신의탑",
    "Summary": "00000000000"
  },
  {
    "Author": "SIU",
    "Title": "신신의의탑",
    "Summary": "00000000000"
  },
  {
    "Author": "IU",
    "Title": "신신의의탑탑",
    "Summary": "00000000000"
  },
  {
    "Author": "자까",
    "Title": "대학일기",
    "Summary": "00000000000"
  },
  {
    "Author": "자까",
    "Title": "대학원일기",
    "Summary": "00000000000"
  },
  {
    "Author": "자까",
    "Title": "중학교일기",
    "Summary": "00000000000"
  },
  {
    "Author": "자까",
    "Title": "고등학교일기",
    "Summary": "00000000000"
  },
  {
    "Author": "자까",
    "Title": "초등학교일기",
    "Summary": "00000000000"
  },
  {
    "Author": "자까",
    "Title": "독립일기",
    "Summary": "00000000000"
  }
]

for i in range(3):
    res = requests.post('http://127.0.0.1:5000/WebToon', files=files[i], data=data_list[i], verify=False)
    sleep(1)
    print(i)
    print(data_list[i], files[i])
print(res.status_code)
print(res.json())