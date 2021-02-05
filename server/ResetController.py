import sys

sys.path.append('../ooapi')

import cherrypy
import json
from tv_library import _tv_database

class ResetController(object):

    def __init__(self, tvdb=None):
        if tvdb is None:
            self.tvdb = _tv_database()
        else:
            self.tvdb = tvdb

    def PUT_INDEX(self):
        '''When a PUT request is made to the /reset/ endpoint, the TV database is reloaded'''
        output = {'result' : 'success'}

        data = json.loads(cherrypy.request.body.read().decode('utf-8'))

        self.tvdb.__init__()
        self.tvdb.load_tv_shows('../ooapi/tv-shows.json')
        self.tvdb.load_users('../ooapi/users.json')

        return json.dumps(output, indent=2)

    def PUT_KEY_TV(self, tvid):
        '''When a PUT request is made to the /reset/tv-shows/tvid endpoint, that TV show is reloaded'''
        output = {'result' : 'success'}
        tvid   = str(tvid)

        try:
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))

            tvdbtmp = _tv_database()
            tvdbtmp.load_tv_shows('../ooapi/tv-shows.json')

            tv_details  = tvdbtmp.get_tv_details(tvid)
            tv_rating   = tvdbtmp.get_tv_rating(tvid)
            tv_summary  = tvdbtmp.get_tv_summary(tvid)
            tv_episodes = tvdbtmp.get_tv_episodes(tvid)

            self.tvdb.set_tv_show(tvid, tv_details, tv_rating, tv_summary, tv_episodes)
        except KeyError as e:
            output['result']  = 'error'
            output['message'] = 'TV show not found'
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        return json.dumps(output, indent=2)

    def PUT_KEY_USER(self, uid):
        '''When a PUT request is made to the /reset/users/uid endpoint, that user is reloaded'''
        output = {'result' : 'success'}
        uid    = str(uid)

        try:
            data = json.loads(cherrypy.request.body.read().decode('utf-8'))

            tvdbtmp = _tv_database()
            tvdbtmp.load_users('../ooapi/users.json')

            user = tvdbtmp.get_user(uid)

            self.tvdb.set_user(uid, user)
        except KeyError as e:
            output['result']  = 'error'
            output['message'] = 'User not found'
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        return json.dumps(output, indent=2)

