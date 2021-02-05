import unittest
import requests
import json

class TestUsersKey(unittest.TestCase):

    SITE_URL  = 'http://localhost:51080'
    USERS_URL = SITE_URL + '/users/'
    RESET_URL = SITE_URL + '/reset/'
    print(f'Testing for server: {SITE_URL} USERS KEY EVENT HANDLERS')

    def reset_data(self):
        m = {}
        r = requests.put(self.RESET_URL, data=json.dumps(m))

    def is_json(self, resp):
        try:
            json.loads(resp)
            return True
        except ValueError:
            return False

    def test_users_get_key(self):
        self.reset_data()
        uid  = 'conor-holahan'
        uid2 = 'nonexistent-user'

        # Check if the response is formatted correctly as JSON
        r = requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r.content.decode('utf-8')))

        # Check if the response is accurate
        resp = json.loads(r.content.decode('utf-8'))
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp[uid]['name'], 'Conor Holahan')
        self.assertEqual(resp[uid]['email'], 'cholahan@nd.edu')
        self.assertEqual(resp[uid]['favorite-genres'], ['Comedy', 'Drama', 'Crime'])

        # Check error handling
        r2 = requests.get(self.USERS_URL + str(uid2))
        self.assertTrue(self.is_json(r2.content.decode('utf-8')))

        # Check if the error response is accurate
        resp2 = json.loads(r2.content.decode('utf-8'))
        self.assertEqual(resp2['result'], 'error')
        self.assertEqual(resp2['message'], 'User not found')

    def test_users_put_key(self):
        self.reset_data()
        uid  = 'conor-holahan'
        uid2 = 'nonexistent-user'
        body = {
                   "email" : "cholahan@gmail.com",
                   "recently-watched" : "rick-and-morty",
                   "preferred-episode-length" : 30,
                   "least-favorite-show": "icarly"
               }

        # Check if the initial response is formatted correctly as JSON
        r_get = requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the initial response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uid]['email'], 'cholahan@nd.edu')
        self.assertEqual(resp_get[uid]['recently-watched'], 'the-wire')
        self.assertEqual(resp_get[uid]['preferred-episode-length'], 60)

        # Check if the PUT response is formatted correctly as JSON
        r_put = requests.put(self.USERS_URL + str(uid), data=json.dumps(body))
        self.assertTrue(self.is_json(r_put.content.decode('utf-8')))

        # Check if the PUT response is accurate
        resp_put = json.loads(r_put.content.decode('utf-8'))
        self.assertEqual(resp_put['result'], 'success')
        self.assertEqual(resp_put['attributes']['email'], 'Changed')
        self.assertEqual(resp_put['attributes']['least-favorite-show'], 'Not changed')

        # Check if the final response is formatted correctly as JSON
        r_get = requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the final response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uid]['email'], 'cholahan@gmail.com')
        self.assertEqual(resp_get[uid]['recently-watched'], 'rick-and-morty')
        self.assertEqual(resp_get[uid]['preferred-episode-length'], 30)

        # Check error handling
        r_put = requests.put(self.USERS_URL + str(uid2), data=json.dumps(body))
        self.assertTrue(self.is_json(r_put.content.decode('utf-8')))

        # Check if the error response is accurate
        resp_put = json.loads(r_put.content.decode('utf-8'))
        self.assertEqual(resp_put['result'], 'error')
        self.assertEqual(resp_put['message'], 'User not found')

    def test_users_delete_key(self):
        self.reset_data()
        uid = 'ryan-destefano'

        # Check that user is initially present
        r_get= requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uid]['name'], 'Ryan DeStefano')
        self.assertEqual(resp_get[uid]['email'], 'rdestefa@nd.edu')

        # Delete user with ID of ryan-destefano
        r_delete = requests.delete(self.USERS_URL + str(uid), data=json.dumps({}))
        self.assertTrue(self.is_json(r_delete.content.decode('utf-8')))

        # Check if DELETE response is accurate
        resp_delete = json.loads(r_delete.content.decode('utf-8'))
        self.assertEqual(resp_delete['result'], 'success')

        # Check if user was deleted
        r_get= requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'error')
        self.assertEqual(resp_get['message'], 'User not found')

        # Check error handling
        r_delete = requests.delete(self.USERS_URL + str(uid), data=json.dumps({}))
        self.assertTrue(self.is_json(r_delete.content.decode('utf-8')))

        # Check if DELETE response is accurate
        resp_delete = json.loads(r_delete.content.decode('utf-8'))
        self.assertEqual(resp_delete['result'], 'error')
        self.assertEqual(resp_delete['message'], 'User not found')
        
if __name__ == '__main__':
    unittest.main()
