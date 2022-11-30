import unittest
import requests
import json

import jwt
from flask_jwt_extended import get_jwt_identity

import config
import ApiDir


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
        for i in range(len(self.RightParam)):
            response = requests.post(
                self.host + '/{}'.format(self.RightParam[i]["ID"]),
                json=self.RightParam[i]
            )
            data = json.loads(response.content)
            self.assertEqual(
                jwt.decode(data, key=config.JWT_SECRET_KEY, algorithms=["HS256"])[
                    "sub"
                ],
                self.RightParam[i]["ID"],
            )

    def testWrongPdParam(self):
        for i in range(len(self.WrongPdParam)):
            response = requests.post(
                self.host + "/{}".format(self.WrongPdParam[i]["ID"]),
                json=self.WrongPdParam[i],
            )
            data = json.loads(response.content)
            self.assertEqual(data, 1)  # 로그인 비밀번호가 틀렸을 때

    def testWrongUserParam(self):
        for i in range(len(self.WrongUserParam)):
            response = requests.post(
                self.host + "/{}".format(self.WrongUserParam[i]["ID"]),
                json=self.WrongUserParam[i],
            )
            data = json.loads(response.content)
            self.assertEqual(data, 2)  # User가 존재하지 않을 때


class UserAddTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/User"
        self.RightParam = [
            {"ID": "test1", "PassWd": "test1", "Age": "22", "Job": "0", "Sex": "0"},
            {"ID": "test2", "PassWd": "test2", "Age": "22", "Job": "0", "Sex": "1"},
        ]
        self.IdExistParam = [ # Id가 이미 존재하는 경우
            {"ID": "ch011015", "PassWd": "1111", "Age": "22", "Job": "0", "Sex": "0"},
            {"ID": "test", "PassWd": "2343", "Age": "22", "Job": "0", "Sex": "0"},
        ]
        self.NotIntParam = [
            {"ID": "test3", "PassWd": "test3", "Age": "hi", "Job": "0", "Sex": "0"},
            {"ID": "test4", "PassWd": "test3", "Age": "22", "Job": "hi", "Sex": "0"},
            {"ID": "test5", "PassWd": "test3", "Age": "22", "Job": "0", "Sex": "hi"},
        ]
    
    @unittest.skip('이미 실행한 테스트, 삽입하는 유저가 이미 존재하므로 해당 유저 삭제 후 진행')
    def testRightCase(self):
        for i in range(len(self.RightParam)):
            response = requests.post(self.host, json=self.RightParam[i])
            data = json.loads(response.content)
            self.assertEqual(data, 0)
    
    def testIdExistCase(self):
        for i in range(len(self.IdExistParam)):
            response = requests.post(self.host, json=self.IdExistParam[i])
            data = json.loads(response.content)
            self.assertEqual(data, 'This User already exist.')

    def testNotIntCase(self):
        for i in range(len(self.NotIntParam)):
            response = requests.post(self.host, json=self.NotIntParam[i])
            data = json.loads(response.content)
            self.assertEqual(data, 'Age, Job, Sex should be integer.')


if __name__ == "__main__":
    unittest.main()