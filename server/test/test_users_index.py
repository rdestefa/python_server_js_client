import unittest
import requests
import json

class TestUsersIndex(unittest.TestCase):
    
    SITE_URL  = 'http://localhost:51080'
    USERS_URL = SITE_URL + '/users/'
    RESET_URL = SITE_URL + '/reset/'
    print(f'Testing for server: {SITE_URL} USERS INDEX EVENT HANDLERS')

    def reset_data(self):
        m = {}
        r = requests.put(self.RESET_URL, data=json.dumps(m))

    def is_json(self, resp):
        try:
            json.loads(resp)
            return True
        except ValueError:
            return False

    def test_users_get_index(self):
        self.reset_data()
        uid = 'ryan-destefano'

        # Check if the response is formatted correctly as JSON
        r = requests.get(self.USERS_URL)
        self.assertTrue(self.is_json(r.content.decode('utf-8')))

        # Check if the response is accurate
        resp = json.loads(r.content.decode('utf-8'))
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['users'].keys()), 2)
        self.assertEqual(resp['users'][uid]['id'], 'ryan-destefano')
        self.assertEqual(resp['users'][uid]['name'], 'Ryan DeStefano')
        self.assertEqual(resp['users'][uid]['recently-watched'], 'the-sopranos')

    def test_users_post_index(self):
        self.reset_data()
        uid   = 'new-user'
        body  = {
                    "name" : "New User",
                    "id" : "new-user",
                    "dob" : "06-16-2000",
                    "email" : "nuser@nd.edu",
                    "favorite-shows" : ["the-legend-of-korra"],
                    "favorite-genres" : ["Action", "Comedy"],
                    "recently-watched" : "drake-and-josh",
                    "best-day-to-watch" : "friday",
                    "preferred-episode-length" : 30
                }
        body2 = {
                    "name" : "New User",
                    "id" : "new-user",
                    "dob" : "06-16-2000",
                    "email" : "nuser@nd.edu",
                }

        # Check if the initial response is formatted correctly as JSON
        r_get = requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the initial response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'error')
        self.assertEqual(resp_get['message'], 'User not found')

        # Check if the POST response is formatted correctly as JSON
        r_post = requests.post(self.USERS_URL, data=json.dumps(body))
        self.assertTrue(self.is_json(r_post.content.decode('utf-8')))

        # Check if the POST response is accurate
        resp_post = json.loads(r_post.content.decode('utf-8'))
        self.assertEqual(resp_post['result'], 'success')
        self.assertEqual(resp_post['id'], 'new-user')

        # Check if the final response is formatted correctly as JSON
        r_get = requests.get(self.USERS_URL + str(uid))
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the final response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertEqual(resp_get[uid]['name'], 'New User')
        self.assertEqual(resp_get[uid]['favorite-genres'], ['Action', 'Comedy'])

        # Check error handling
        r_post = requests.post(self.USERS_URL, data=json.dumps(body2))
        self.assertTrue(self.is_json(r_post.content.decode('utf-8')))
    
        # Check if the error response is accurate
        resp_post = json.loads(r_post.content.decode('utf-8'))
        self.assertEqual(resp_post['result'], 'error')
        self.assertEqual(resp_post['message'], 'User not added. Check that body of request contains the following keys: name, id, dob, email, favorite-shows, favorite-genres, recently-watched, best-day-to-watch, preferred-episode-length')

    def test_users_delete_index(self):
        self.reset_data()

        # Check if users are initially present
        r_get = requests.get(self.USERS_URL)
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertTrue(resp_get['users'])
        self.assertEqual(resp_get['users']['ryan-destefano']['name'], 'Ryan DeStefano')

        # Delete users
        r_delete = requests.delete(self.USERS_URL)
        self.assertTrue(self.is_json(r_delete.content.decode('utf-8')))

        # Check if the DELETE response is accurate
        resp_delete = json.loads(r_delete.content.decode('utf-8'))
        self.assertEqual(resp_delete['result'], 'success')

        # Check if users were deleted
        r_get = requests.get(self.USERS_URL)
        self.assertTrue(self.is_json(r_get.content.decode('utf-8')))

        # Check if the GET response is accurate
        resp_get = json.loads(r_get.content.decode('utf-8'))
        self.assertEqual(resp_get['result'], 'success')
        self.assertFalse(resp_get['users'])

if __name__ == '__main__':
    unittest.main()
