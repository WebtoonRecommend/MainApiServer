import unittest
import requests
import json

import jwt
from flask_jwt_extended import get_jwt_identity

import config
import ApiDir
import test_func


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


class UserAddTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/User"
        self.RightParam = [
            {"ID": "test1", "PassWd": "test1", "Age": "22", "Job": "0", "Sex": "0"},
            {"ID": "test2", "PassWd": "test2", "Age": "22", "Job": "0", "Sex": "1"},
        ]
        self.IdExistParam = [  # Id가 이미 존재하는 경우
            {"ID": "ch011015", "PassWd": "1111", "Age": "22", "Job": "0", "Sex": "0"},
            {"ID": "test", "PassWd": "2343", "Age": "22", "Job": "0", "Sex": "0"},
        ]
        self.NotIntParam = [
            {"ID": "test4", "PassWd": "test3", "Age": "22", "Job": "hi", "Sex": "0"},
            {"ID": "test5", "PassWd": "test3", "Age": "22", "Job": "0", "Sex": "hi"},
        ]

    @unittest.skip("이미 실행한 테스트, 삽입하는 유저가 이미 존재하므로 해당 유저 삭제 후 진행")
    def testRightCase(self):
        for i in self.RightParam:
            response = requests.post(self.host, json=i)
            data = json.loads(response.content)
            self.assertEqual(data, 0)

    def testIdExistCase(self):
        for i in self.IdExistParam:
            response = requests.post(self.host, json=i)
            data = json.loads(response.content)
            self.assertEqual(data, "This User already exist.")

    def testNotIntCase(self):
        for i in self.NotIntParam:
            response = requests.post(self.host, json=i)
            data = json.loads(response.content)
            self.assertEqual(data, "Age, Job, Sex should be integer.")


class UserGetTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/User"
        self.IdNotExistParam = [
            {"ID": "test6", "PassWd": "1111", "Age": "22", "Job": "0", "Sex": "0"},
            {"ID": "test7", "PassWd": "2343", "Age": "22", "Job": "0", "Sex": "0"},
        ]
        self.IdExistParam = [
            {"ID": "test1", "PassWd": "test1", "Age": "22", "Job": "0", "Sex": "0"},
            {"ID": "test2", "PassWd": "test2", "Age": "22", "Job": "0", "Sex": "1"},
        ]

        # api 테스트를 위한 jwt 토큰 저장
        self.jwt_l = {}
        for i in self.IdExistParam:
            self.jwt_l[i["ID"]] = json.loads(
                requests.post(
                    self.host + "/{}".format(i["ID"]),
                    json=i,
                ).content
            )

    def testGetUserExist(self):
        for i in self.IdExistParam:
            response = requests.get(
                self.host + "/{}".format(i["ID"]),
                headers={"Authorization": "Bearer " + self.jwt_l[i["ID"]]},
            )
            data = json.loads(response.content)
            self.assertEqual(data["Age"], int(i["Age"]))
            self.assertEqual(data["Job"], int(i["Job"]))
            self.assertEqual(data["Sex"], int(i["Sex"]))

    def testGetUserNotExist(self):
        for i in self.IdNotExistParam:
            response = requests.get(
                self.host + "/{}".format(i["ID"]),
                headers={"Authorization": "Bearer " + self.jwt_l["test1"]},
            )  # 타인의 jwt로 정보 획득 시도
            data = json.loads(response.content)
            self.assertEqual(data, "This User doesn't exist")


class KeyWordGetTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/KeyWords"
        self.KeyWordEmptyParam = [
            {"ID": "test2", "PassWd": "test2"},
            {"ID": "test3", "PassWd": "test3"},
        ]
        self.KeyWordOnlyParam = [
            {"ID": "test", "PassWd": "test"},
        ]

        self.jwt_l = {}

        self.jwt_l = test_func.get_jwt(self.KeyWordEmptyParam, self.jwt_l)
        self.jwt_l = test_func.get_jwt(self.KeyWordOnlyParam, self.jwt_l)

    def testGetKeyWordOnlyCase(self):
        for i in self.KeyWordOnlyParam:
            response = requests.get(
                self.host, headers={"Authorization": "Bearer " + self.jwt_l[i["ID"]]}
            )
            data = json.loads(response.content)
            self.assertNotEqual(len(data), 0)

    def testGetKeyWordEmptyCase(self):
        for i in self.KeyWordEmptyParam:
            response = requests.get(
                self.host,
                headers={"Authorization": "Bearer " + self.jwt_l[i["ID"]]},
            )
            data = json.loads(response.content)
            self.assertEqual(data, "You don't add any Keyword. Please add Keyword.")


# class KeyWordPostTest(unittest.TestCase):
#     def setUp(self):


class RecommendTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/Recommended/"
        self.BookMarkExistParam = [
            {"ID": "ch011015", "PassWd": "011015", "Days": "0"},
        ]
        self.KeyWordExistParam = [
            {"ID": "test", "PassWd": "test", "Days": "0"},
            {"ID": "test1", "PassWd": "test1", "Days": "1"},
        ]
        self.NothingExistParam = [
            {"ID": "test2", "PassWd": "test2"},
            {"ID": "test3", "PassWd": "test3"},
        ]

        self.jwts = {}

        self.jwts = test_func.get_jwt(self.BookMarkExistParam, self.jwts)
        self.jwts = test_func.get_jwt(self.KeyWordExistParam, self.jwts)
        self.jwts = test_func.get_jwt(self.NothingExistParam, self.jwts)

    # 북마크 기반 추천
    def testBookMarkRecommend(self):
        for i in self.BookMarkExistParam:
            response = requests.get(
                self.host + "{}".format(i["Days"]),
                headers={"Authorization": "Bearer " + self.jwts[i["ID"]]},
            )
            data = json.loads(response.content)
            self.assertEqual(type(data), type([]))
            self.assertNotEqual(len(data), 0)

    # 키워드 기반 추천
    def testKeyWordRecommend(self):
        for i in self.KeyWordExistParam:
            response = requests.get(
                self.host + "{}".format(i["Days"]),
                headers={"Authorization": "Bearer " + self.jwts[i["ID"]]},
            )
            data = json.loads(response.content)
            self.assertEqual(type(data), type([]))
            self.assertNotEqual(len(data), 0)

    def testNothingExist(self):
        for i in self.NothingExistParam:
            response = requests.get(
                self.host + "{}".format("0"),
                headers={"Authorization": "Bearer " + self.jwts[i["ID"]]},
            )
            data = json.loads(response.content)
            self.assertEqual(data, "This User doesn't add KeyWord")

    def testErrorDays(self):
        for i in self.KeyWordExistParam:
            response = requests.get(
                self.host + "{}".format("a"),
                headers={"Authorization": "Bearer " + self.jwts[i["ID"]]},
            )
            data = json.loads(response.content)
            self.assertEqual(data, "Please enter a 'Only Number' for days")


if __name__ == "__main__":
    unittest.main()
