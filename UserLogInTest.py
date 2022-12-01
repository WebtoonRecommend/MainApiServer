import unittest
import requests
import json

import jwt
from flask_jwt_extended import get_jwt_identity

import config


# UserApi 테스트 코드
class UserLogInTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/User"
        self.RightParam = [
            {"ID": "ch011015", "PassWd": "011015"},
            {"ID": "test", "PassWd": "test"},
        ]
        self.WrongPdParam = [
            {"ID": "ch011015", "PassWd": "1111"},
            {"ID": "test", "PassWd": "2343"},
        ]
        self.WrongUserParam = [
            {"ID": "ch01101", "PassWd": "1111"},
            {"ID": "nvoawienlgfka", "PassWd": "2343"},
        ]

    def testRightParam(self):
        for i in self.RightParam:
            response = requests.post(
                self.host + "/{}".format(i["ID"]),
                json=i,
            )
            data = json.loads(response.content)
            self.assertEqual(
                jwt.decode(data, key=config.JWT_SECRET_KEY, algorithms=["HS256"])[
                    "sub"
                ],
                i["ID"],
            )

    def testWrongPdParam(self):
        for i in self.WrongPdParam:
            response = requests.post(
                self.host + "/{}".format(i["ID"]),
                json=i,
            )
            data = json.loads(response.content)
            self.assertEqual(data, 1)  # 로그인 비밀번호가 틀렸을 때

    def testWrongUserParam(self):
        for i in self.WrongUserParam:
            response = requests.post(
                self.host + "/{}".format(i["ID"]),
                json=i,
            )
            data = json.loads(response.content)
            self.assertEqual(data, 2)  # User가 존재하지 않을 때


if __name__ == "__main__":
    unittest.main()
