import unittest
import requests
import json

import jwt
from flask_jwt_extended import get_jwt_identity

import test_func


class WetToonGetTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/WebToon/"
        self.WrongTitle = [
            {"ID": "ch011015", "PassWd": "011015", "Title": "title"},
            {"ID": "ch011015", "PassWd": "011015", "Title": "title1"},
        ]
        self.RightTitle = [
            {"ID": "ch011015", "PassWd": "011015", "Title": "대학일기"},
            {"ID": "ch011015", "PassWd": "011015", "Title": "나노리스트"},
        ]

        self.jwt_l = {}
        test_func.get_jwt(
            [{"ID": "ch011015", "PassWd": "011015", "Title": "title"}], self.jwt_l
        )

    def testWrongTitle(self):
        for i in self.WrongTitle:
            response = requests.get(
                self.host + "{}".format(i["Title"]),
                headers={"Authorization": "Bearer {}".format(self.jwt_l["ch011015"])},
            )
            data = json.loads(response.content)
            self.assertEqual(data, "Wrong Webtoon Title")

    def testRightTitle(self):
        for i in self.RightTitle:
            response = requests.get(
                self.host + "{}".format(i["Title"]),
                headers={"Authorization": "Bearer {}".format(self.jwt_l["ch011015"])},
            )
            data = json.loads(response.content)
            self.assertNotEqual(data, "Wrong Webtoon Title")
            self.assertEqual(type(data), type({}))


if __name__ == "__main__":
    unittest.main()
