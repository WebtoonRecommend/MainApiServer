import unittest
import requests
import json

import test_func


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
