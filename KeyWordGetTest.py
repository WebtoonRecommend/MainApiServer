import unittest
import requests
import json

import test_func


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


if __name__ == "__main__":
    unittest.main()
