import unittest
import requests
import json

class TestReset(unittest.TestCase):

    SITE_URL        = 'http://localhost:51080'
    TV_URL          = SITE_URL  + '/tv-shows/'
    USERS_URL       = SITE_URL  + '/users/'
    RESET_URL       = SITE_URL  + '/reset/'
    RESET_TV_URL    = RESET_URL + 'tv-shows/'
    RESET_USERS_URL = RESET_URL + 'users/'
    print(f'Testing for server: {SITE_URL} RESET EVENT HANDLERS')

    def is_json(self, resp):
        try:
            json.loads(resp)
            return True
        except ValueError:
            return False

    def test_reset_put_index(self):
        uids  = ['ryan-destefano', 'conor-holahan']
        bodys = [{
                     "email" : "rdestefa@gmail.com",
                     "recently-watched" : "dragon-ball-super"
                 },
                 {
                     "email" : "cholahan@gmail.com",
                     "recently-watched" : "the-office"
                 }]

        # Change user with ID of ryan-destefano
        r_put = requests.put(self.USERS_URL + str(uids[0]), data=json.dumps(bodys[0]))
        self.assertTrue(self.is_json(r_put.content.decode('utf-8')))

        # Check that the PUT response is accurate
        resp_put = json.loads(r_put.content.decode('utf-8'))
        self.assertEqual(resp_put['result'], 'success')

        # Check that the user was changed
        r_get = requests.get(self.USERS_URL + str(uids[0]))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check the the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uids[0]]['email'], 'rdestefa@gmail.com')
        self.assertEqual(resp_get[uids[0]]['recently-watched'], 'dragon-ball-super')

        # Change user with ID of conor-holahan
        r_put = requests.put(self.USERS_URL + str(uids[1]), data=json.dumps(bodys[1]))
        self.assertTrue(self.is_json(r_put.content.decode('utf-8')))

        # Check that the PUT response is accurate
        resp_put = json.loads(r_put.content.decode('utf-8'))
        self.assertEqual(resp_put['result'], 'success')

        # Check that the user was changed
        r_get = requests.get(self.USERS_URL + str(uids[1]))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check the the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uids[1]]['email'], 'cholahan@gmail.com')
        self.assertEqual(resp_get[uids[1]]['recently-watched'], 'the-office')

        # Reset users
        r_reset = requests.put(self.RESET_URL, data=json.dumps({}))
        self.assertTrue(self.is_json(r_reset.content.decode('utf-8')))

        # Check that the reset response is accurate
        resp_reset = json.loads(r_reset.content.decode('utf-8'))
        self.assertEqual(resp_reset['result'], 'success')

        # Check user with ID of ryan-destefano
        r_get = requests.get(self.USERS_URL + str(uids[0]))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check that the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uids[0]]['email'], 'rdestefa@nd.edu')
        self.assertEqual(resp_get[uids[0]]['recently-watched'], 'the-sopranos')
        
        # Check user with ID of conor-holahan
        r_get = requests.get(self.USERS_URL + str(uids[1]))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check that the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uids[1]]['email'], 'cholahan@nd.edu')
        self.assertEqual(resp_get[uids[1]]['recently-watched'], 'the-wire')

    def test_reset_put_key_user(self):
        uid  = 'ryan-destefano'
        body = {
                    "email" : "rdestefa@gmail.com",
                    "recently-watched" : "dragon-ball-super"
               }

        # Change user with ID of ryan-destefano
        r_put = requests.put(self.USERS_URL + str(uid), data=json.dumps(body))
        self.assertTrue(self.is_json(r_put.content.decode('utf-8')))

        # Check that the PUT response is accurate
        resp_put = json.loads(r_put.content.decode('utf-8'))
        self.assertEqual(resp_put['result'], 'success')

        # Check that the user was changed
        r_get = requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check the the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uid]['email'], 'rdestefa@gmail.com')
        self.assertEqual(resp_get[uid]['recently-watched'], 'dragon-ball-super')

        # Reset user
        r_reset = requests.put(self.RESET_USERS_URL + str(uid), data=json.dumps({}))
        self.assertTrue(self.is_json(r_reset.content.decode('utf-8')))

        # Check that the reset response is accurate
        resp_reset = json.loads(r_reset.content.decode('utf-8'))
        self.assertEqual(resp_reset['result'], 'success')

        # Check user with ID of ryan-destefano
        r_get = requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check that the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uid]['email'], 'rdestefa@nd.edu')
        self.assertEqual(resp_get[uid]['recently-watched'], 'the-sopranos')

if __name__ == '__main__':
    unittest.main()
