import unittest
import requests
import json


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


if __name__ == "__main__":
    unittest.main()
