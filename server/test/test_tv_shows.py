import unittest
import requests
import json

class TestMovies(unittest.TestCase):

    SITE_URL  = 'http://localhost:51080'
    TV_URL    = SITE_URL + '/tv-shows/'
    RESET_URL = SITE_URL + '/reset/'
    print(f'Testing for server: {SITE_URL} TV SHOWS EVENT HANDLERS')

    def reset_data(self):
        m = {}
        r = requests.put(self.RESET_URL, data=json.dumps(m))

    def is_json(self, resp):
        try:
            json.loads(resp)
            return True
        except ValueError:
            return False

    def test_tv_get_key(self):
        self.reset_data()
        tvid  = 'avatar-the-last-airbender'
        tvid2 = 'spongebob-rectanglepants'

        # Check if the response is formatted correctly as JSON
        r = requests.get(self.TV_URL + str(tvid))
        self.assertTrue(self.is_json(r.content.decode('utf-8')))

        # Check if the response is accurate
        resp = json.loads(r.content.decode('utf-8'))
        self.assertEqual(resp[tvid]['details']['name'], 'Avatar: The Last Airbender')
        self.assertEqual(resp[tvid]['details']['genres'], ['Action', 'Adventure', 'Fantasy'])
        self.assertEqual(resp[tvid]['rating'], 8.9)
        self.assertEqual(resp[tvid]['summary']['website'], 'https://www.nick.com/shows/avatar')
        self.assertEqual(len(resp[tvid]['episodes']), 61)

        # Check error handling
        r2 = requests.get(self.TV_URL + str(tvid2))
        self.assertTrue(self.is_json(r2.content.decode('utf-8')))
        
        # Check if the error response is accurate
        resp2 = json.loads(r2.content.decode('utf-8'))
        self.assertEqual(resp2['result'], 'error')
        self.assertEqual(resp2['message'], 'TV show not found')

    def test_tv_get_index(self):
        self.reset_data()
    
        # Check if the response is formatted correctly as JSON
        r = requests.get(self.TV_URL)
        self.assertTrue(self.is_json(r.content.decode('utf-8')))

        # Check if the response is accurate
        resp = json.loads(r.content.decode('utf-8'))
        self.assertEqual(len(resp['tv-shows']), 38)

        for tv_show in resp['tv-shows']:
            if tv_show['details']['id'] == 'the-sopranos':
                test_tv_show = tv_show

        self.assertEqual(test_tv_show['details']['name'], 'The Sopranos')
        self.assertEqual(test_tv_show['rating'], 9.1)
        self.assertEqual(test_tv_show['summary']['website'], 'http://www.hbo.com/the-sopranos')
        self.assertEqual(len(test_tv_show['episodes']), 86)

if __name__ == '__main__':
    unittest.main()
