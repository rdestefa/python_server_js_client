import sys

sys.path.append('../')

import unittest
import json
from tv_library import _tv_database

class TestTVLibrary(unittest.TestCase):

    TV_PATH    = '../tv-shows.json'
    USERS_PATH = '../users.json'
    print('Testing _tv_database')

    def load_database(self):
        tvdb = _tv_database()
        tvdb.load_tv_shows(self.TV_PATH)
        tvdb.load_users(self.USERS_PATH)

        return tvdb

    def test_get_tv_shows(self):
        tvdb  = self.load_database()
        shows = tvdb.get_tv_shows()

        # Check that shows contains accurate information
        self.assertEqual(len(shows), 38)
        self.assertTrue('the-sopranos' in shows)
        self.assertTrue('the-wire' in shows)
        self.assertTrue('avatar-the-last-airbender' in shows)

    def test_get_tv_details_key(self):
        tvdb     = self.load_database()
        show     = tvdb.get_tv_details('avatar-the-last-airbender')
        bad_show = tvdb.get_tv_details('avatar-the-last-codebender')

        # Check that show contains accurate information
        self.assertEqual(show['id'], 'avatar-the-last-airbender')
        self.assertEqual(show['name'], 'Avatar: The Last Airbender')
        self.assertEqual(show['episode-length'], 30)
        self.assertEqual(show['genres'], ['Action', 'Adventure', 'Fantasy'])

        # Check error handling
        self.assertFalse(bad_show)

    def test_get_tv_details_index(self):
        tvdb  = self.load_database()
        shows = tvdb.get_tv_details()

        # Check that shows contains accurate information
        self.assertEqual(shows['the-office']['name'], 'The Office')
        self.assertEqual(shows['the-office']['episode-length'], 30)
        self.assertEqual(shows['the-office']['genres'], ['Comedy'])
        self.assertEqual(shows['spongebob-squarepants']['name'], 'SpongeBob SquarePants')
        self.assertEqual(shows['spongebob-squarepants']['episode-length'], 15)
        self.assertEqual(shows['spongebob-squarepants']['genres'], ['Comedy', 'Children'])

    def test_get_tv_rating_key(self):
        tvdb       = self.load_database()
        rating     = tvdb.get_tv_rating('the-sopranos')
        bad_rating = tvdb.get_tv_rating('the-tenors')

        # Check that rating contains accurate information
        self.assertEqual(rating, 9.1)

        # Check error handling
        self.assertFalse(bad_rating)

    def test_get_tv_rating_index(self):
        tvdb    = self.load_database()
        ratings = tvdb.get_tv_rating()

        # Check that ratings contains accurate information
        self.assertEqual(ratings['the-wire'], 9.1)
        self.assertEqual(ratings['30-rock'], 8.2)

    def test_get_tv_summary_key(self):
        tvdb        = self.load_database()
        summary     = tvdb.get_tv_summary('fullmetal-alchemist-brotherhood')
        bad_summary = tvdb.get_tv_summary('fullmetal-alchemist-sisterhood')

        # Check that summary contains accurate information
        self.assertFalse(summary['website'])
        self.assertEqual(summary['images']['medium'], 'http://static.tvmaze.com/uploads/images/medium_portrait/11/28760.jpg')

        # Check error handling
        self.assertFalse(bad_summary)

    def test_get_tv_summary_index(self):
        tvdb      = self.load_database()
        summaries = tvdb.get_tv_summary()

        # Check that summaries contains accurate information
        self.assertEqual(summaries['my-hero-academia']['website'], 'http://heroaca.com/')
        self.assertEqual(summaries['my-hero-academia']['images']['regular'], 'http://static.tvmaze.com/uploads/images/original_untouched/65/164727.jpg')
        self.assertEqual(summaries['south-park']['website'], 'http://southpark.cc.com')
        self.assertEqual(summaries['south-park']['images']['medium'], 'http://static.tvmaze.com/uploads/images/medium_portrait/0/935.jpg')

    def test_get_tv_episodes_key(self):
        tvdb         = self.load_database()
        episodes     = tvdb.get_tv_episodes('the-legend-of-korra')
        bad_episodes = tvdb.get_tv_episodes('the-tale-of-korra')

        # Check that episodes contains accurate information
        self.assertEqual(episodes[0]['name'], 'Welcome to Republic City')
        self.assertEqual(episodes[1]['airdate'], '2012-04-14')
        self.assertEqual(episodes[6]['number'], 7)

        # Check error handling
        self.assertFalse(bad_episodes)

    def test_get_tv_episodes_index(self):
        tvdb     = self.load_database()
        episodes = tvdb.get_tv_episodes()

        # Check that episodes contains accurate information
        self.assertEqual(episodes['rick-and-morty'][1]['name'], 'Lawnmower Dog')
        self.assertEqual(episodes['rick-and-morty'][2]['id'], 14310)
        self.assertEqual(episodes['the-big-bang-theory'][3]['name'], 'The Luminous Fish Effect')
        self.assertEqual(episodes['the-big-bang-theory'][4]['id'], 2917)

    def test_get_users(self):
        tvdb  = self.load_database()
        users = tvdb.get_users()

        # Check that users contains accurate information
        self.assertTrue('ryan-destefano' in users)
        self.assertTrue('conor-holahan' in users)

    def test_get_user_key(self):
        tvdb     = self.load_database()
        user     = tvdb.get_user('ryan-destefano')
        bad_user = tvdb.get_user('r-destefano') 

        # Check that user contains accurate information
        self.assertEqual(user['name'], 'Ryan DeStefano')
        self.assertEqual(user['dob'], '07-16-2000')
        self.assertEqual(user['email'], 'rdestefa@nd.edu')

        # Check error handling
        self.assertFalse(bad_user)

    def test_get_user_index(self):
        tvdb  = self.load_database()
        users = tvdb.get_user()

        # Check that users contains accurate information
        self.assertEqual(users['ryan-destefano']['name'], 'Ryan DeStefano')
        self.assertEqual(users['ryan-destefano']['email'], 'rdestefa@nd.edu')
        self.assertEqual(users['conor-holahan']['name'], 'Conor Holahan')
        self.assertEqual(users['conor-holahan']['email'], 'cholahan@nd.edu')

    def test_set_attribute(self):
        tvdb = self.load_database()
        user = tvdb.get_user('conor-holahan')

        # Check that user initially contains accurate information
        self.assertEqual(user['recently-watched'], 'the-wire')

        # Change value of user['recently-watched']
        tvdb.set_attribute('conor-holahan', 'recently-watched', 'the-sopranos')

        # Check that user contains accurate information
        user = tvdb.get_user('conor-holahan')
        self.assertEqual(user['recently-watched'], 'the-sopranos')

    def test_set_user(self):
        tvdb    = self.load_database()
        user    = tvdb.get_user('nonexistent-user')
        details = {
                      "name" : "Nonexistent User",
                      "id" : "nonexistent-user",
                      "dob" : "06-16-2000",
                      "email" : "nuser@nd.edu",
                      "favorite-shows" : [
                          "30-rock",
                          "spongebob-squarepants",
                          "dragon-ball-z"
                      ],
                      "favorite-genres" : [
                          "Action",
                          "Comedy",
                          "Drama"
                      ],
                      "recently-watched" : "rick-and-morty",
                      "best-day-to-watch": "monday",
                      "preferred-episode-length" : 30
                  }

        # Check that user initially doesn't exist
        self.assertFalse(user)

        # Add new user
        tvdb.set_user('nonexistent-user', details)

        # Check that user contains accurate information
        user = tvdb.get_user('nonexistent-user')
        self.assertEqual(user['name'], 'Nonexistent User')
        self.assertEqual(user['email'], 'nuser@nd.edu')
        self.assertEqual(user['favorite-genres'], ['Action', 'Comedy', 'Drama'])

if __name__ == '__main__':
    unittest.main()
