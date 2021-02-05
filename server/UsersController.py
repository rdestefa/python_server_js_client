import sys

sys.path.append('../ooapi')

import cherrypy
import json
from tv_library import _tv_database

class UsersController(object):

    # Constructor
    def __init__(self, tvdb=None):
        if tvdb is None:
            self.tvdb = _tv_database()
        else:
            self.tvdb = tvdb

        self.tvdb.load_users('../ooapi/users.json')

    def GET_KEY(self, uid):
        '''When a GET request is made to /users/uid, send a response as a JSON string'''
        output = {'result' : 'success'}
        uid    = str(uid)

        try:
            # Initialize dictionary
            output[uid] = {}

            # Get all necessary data from tvdb
            user = self.tvdb.get_user(uid)

            if user is not None:
                # Populate the output response
                output[uid] = user
            else:
                output['result']  = 'error'
                output['message'] = 'User not found'
        # Handle errors
        except KeyError as e:
            output['result']  = 'error'
            output['message'] = 'User not found'
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)

    def PUT_KEY(self, uid):
        '''When a PUT request is made to /users/uid, change that user in the tvdb'''
        output = {'result'     : 'success',
                  'attributes' : {}}
        uid    = str(uid)

        # Read in body from request
        data = json.loads(cherrypy.request.body.read().decode('utf-8'))

        keys = ('name', 'id', 'dob', 'email', 'favorite-shows', 'favorite-genres', 'recently-watched', 'best-day-to-watch', 'preferred-episode-length')

        try:
            # Check if user exists
            if uid in self.tvdb.get_users():
                # Loop through and update each attribute of the user
                for key in data.keys():
                    if key in keys:
                        self.tvdb.set_attribute(uid, key, data[key])
                        output['attributes'][key] = 'Changed'
                    else:
                        output['attributes'][key] = 'Not changed'
            else:
                output['result']  = 'error'
                output['message'] = 'User not found'
        # Handle errors
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)

    def DELETE_KEY(self, uid):
        '''When a DELETE request is made to /users/uid, remove that user from the tvdb'''
        output = {'result' : 'success'}
        uid    = str(uid)

        try:
            # Delete user from users dictionary in tvdb
            del self.tvdb.users[uid]
        # Handle errors
        except KeyError as e:
            output['result']  = 'error'
            output['message'] = 'User not found'
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)
            
    def GET_INDEX(self):
        '''When a GET request is made to /users/, send a response as a JSON string'''
        output          = {'result' : 'success'}
        output['users'] = {}

        try:
            # Get all necessary data from tvdb
            users = self.tvdb.get_user()

            # Populate the output response
            output['users'] = users
        # Handle errors
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)

    def POST_INDEX(self):
        '''When a POST request is made to /users/, create a new user from body of request'''
        output = {'result' : 'success'}

        # Read in body from request
        data = json.loads(cherrypy.request.body.read().decode('utf-8'))

        keys = ['name', 'id', 'dob', 'email', 'favorite-shows', 'favorite-genres', 'recently-watched', 'best-day-to-watch', 'preferred-episode-length']

        try:
            # Create new user
            if set(keys) == set(data.keys()):
                uid = str(data['id'])
                self.tvdb.set_user(uid, data)
                output['id'] = uid
            else:
                output['result']  = 'error'
                error_string      = 'User not added. Check that body of request contains the following keys: name'
                for key in keys[1:]:
                    error_string = error_string + ', ' + str(key)
                output['message'] = error_string
        # Handle errors
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)
        
    def DELETE_INDEX(self):
        '''When a DELETE request is made to /users/, remove each existing user from the tvdb'''
        output = {'result' : 'success'}

        try:
            # Clear dictionary of users from tvdb
            self.tvdb.users.clear()
        # Handle errors
        except Exception as e:
            output['result']  = 'error'
            output['message'] = str(e)

        # Send response
        return json.dumps(output, indent=2)

