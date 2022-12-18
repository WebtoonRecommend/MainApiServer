import unittest
import requests
import json

import jwt
from flask_jwt_extended import get_jwt_identity

import test_func


class WetToonSearchTest(unittest.TestCase):
    def setUp(self):
        self.host = "http://127.0.0.1:5001/WebToon/Search/"
        self.ShortTitle = [
            {"ID": "ch011015", "PassWd": "011015", "Title": "가"},
            {"ID": "ch011015", "PassWd": "011015", "Title": "대학"},
        ]
        self.SQLInjection = [
            {
                "ID": "ch011015",
                "PassWd": "011015",
                "Title": "'; DROP TABLE webtoonInfoJoin;",
            },
        ]

        self.jwt_l = {}
        test_func.get_jwt([{"ID": "ch011015", "PassWd": "011015"}], self.jwt_l)

    def testShortTitle(self):
        for i in self.ShortTitle:
            response = requests.get(
                self.host + "{}".format(i["Title"]),
                headers={"Authorization": "Bearer {}".format(self.jwt_l["ch011015"])},
            )
            data = json.loads(response.content)
            self.assertEqual(type(data), type([]))

    def testSQLInjection(self):
        for i in self.SQLInjection:
            response = requests.get(
                self.host + "{}".format(i["Title"]),
                headers={"Authorization": "Bearer {}".format(self.jwt_l["ch011015"])},
            )
            data = json.loads(response.content)
            self.assertEqual(type(data), type([]))


if __name__ == "__main__":
    unittest.main()
