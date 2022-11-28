import unittest
import requests
import json

import jwt
from flask_jwt_extended import get_jwt_identity
import jsonify

import config
import ApiDir


# UserApi 테스트 코드
class UserLogInTest(unittest.TestCase):

    def setUp(self):
        self.host = 'http://127.0.0.1:5001/User'
        self.right_param = [
                {'ID':'ch011015', 'PassWd':"011015"},
                {'ID':'test', 'PassWd':"test"}
            ]
        self.wrong_param = [
                {'ID':'ch011015', 'PassWd':'1111'},
                {'ID':'nvoawienlgfka', 'PassWd':'2343'},
            ]
        
    def testRightParam(self):
        for i in range(len(self.right_param)):
            response = requests.post(self.host+'/{}'.format(self.right_param[i]['ID']), json=self.right_param[i])
            data = json.loads(response.content)
            self.assertEqual(jwt.decode(data, key=config.JWT_SECRET_KEY, algorithms=["HS256"])['sub'], self.right_param[i]['ID'])


if __name__ == '__main__':
    unittest.main()