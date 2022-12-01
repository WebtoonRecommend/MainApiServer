import unittest
import requests
import json


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


if __name__ == "__main__":
    unittest.main()
