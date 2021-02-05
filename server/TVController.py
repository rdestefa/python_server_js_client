import sys

sys.path.append('../ooapi')

import cherrypy
import json
from tv_library import _tv_database

class TVController(object):

    # Constructor
    def __init__(self, tvdb=None):
        if tvdb is None:
            self.tvdb = _tv_database()
        else:
            self.tvdb = tvdb

        self.tvdb.load_tv_shows('../ooapi/tv-shows.json')

    def GET_KEY(self, tvid):
        '''When a GET request is made to /tv-shows/tv_id, send a response as a JSON string'''
        output = {'result' : 'success'}
        tvid   = str(tvid)

        try:
            # Initialize dictionary
            output[tvid] = {}

            # Get all necessary data from tvdb
            details  = self.tvdb.get_tv_details(tvid)
            rating   = self.tvdb.get_tv_rating(tvid)
            summary  = self.tvdb.get_tv_summary(tvid)
            episodes = self.tvdb.get_tv_episodes(tvid)

            if None not in (details, rating, summary, episodes):
                # Populate the output response
                output[tvid]['details']  = details
                output[tvid]['summary']  = summary
                output[tvid]['rating']   = rating
                output[tvid]['episodes'] = episodes
            else:
                output['result']  = 'error'
                output['message'] = 'TV show not found'
        # Handle errors
        except KeyError as e:
            output['result']  = 'error'
            output['message'] = 'TV show not found'
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)

    def GET_INDEX(self):
        '''When a GET request is made to /tv-shows/, send a response as a JSON string'''
        output             = {'result' : 'success'}
        output['tv-shows'] = []

        try:
            # Get all necessary data from tvdb
            details   = self.tvdb.get_tv_details()
            ratings   = self.tvdb.get_tv_rating()
            summaries = self.tvdb.get_tv_summary()
            episodes  = self.tvdb.get_tv_episodes()

            # Populate the output response
            for tvid in self.tvdb.get_tv_shows():
                tvtmp = {
                            'details'  : details[tvid],
                            'rating'   : ratings[tvid],
                            'summary'  : summaries[tvid],
                            'episodes' : episodes[tvid]
                        }
                output['tv-shows'].append(tvtmp)
        # Handle errors
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)

