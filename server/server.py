# Ryan DeStefano (rdestefa)
# Conor Holahan  (cholahan)

import sys

sys.path.append('../ooapi')

import cherrypy
from TVController import TVController
from UsersController import UsersController
from ResetController import ResetController
from tv_library import _tv_database

class optionsController:
    def OPTIONS(self, *args, **kwargs):
        return ""

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true"

def start_service():
    dispatcher = cherrypy.dispatch.RoutesDispatcher()

    tvdb = _tv_database()

    tvController    = TVController(tvdb=tvdb)
    usersController = UsersController(tvdb=tvdb)
    resetController = ResetController(tvdb=tvdb) 

    # TV show event handlers
    dispatcher.connect('tv_get', '/tv-shows/:tvid', controller=tvController, action='GET_KEY', conditions=dict(method=['GET']))
    dispatcher.connect('tv_index_get', '/tv-shows/', controller=tvController, action='GET_INDEX', conditions=dict(method=['GET']))

    # Users event handlers
    dispatcher.connect('users_get', '/users/:uid', controller=usersController, action='GET_KEY', conditions=dict(method=['GET']))
    dispatcher.connect('users_put', '/users/:uid', controller=usersController, action='PUT_KEY', conditions=dict(method=['PUT']))
    dispatcher.connect('users_delete', '/users/:uid', controller=usersController, action='DELETE_KEY', conditions=dict(method=['DELETE']))
    dispatcher.connect('users_index_get', '/users/', controller=usersController, action='GET_INDEX', conditions=dict(method=['GET']))
    dispatcher.connect('users_index_post', '/users/', controller=usersController, action='POST_INDEX', conditions=dict(method=['POST']))
    dispatcher.connect('users_index_delete', '/users/', controller=usersController, action='DELETE_INDEX', conditions=dict(method=['DELETE']))

    # Reset event handlers
    dispatcher.connect('reset_put_tv', '/reset/tv-shows/:tvid', controller=resetController, action='PUT_KEY_TV', conditions=dict(method=['PUT']))
    dispatcher.connect('reset_put_user', '/reset/users/:uid', controller=resetController, action='PUT_KEY_USER', conditions=dict(method=['PUT']))
    dispatcher.connect('reset_index_put', '/reset/', controller=resetController, action='PUT_INDEX', conditions=dict(method=['PUT']))

    # CORS related options connections
    dispatcher.connect('tv_options', '/tv-shows/:tvid', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('tv_index_options', '/tv-shows/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('users_options', '/users/:uid', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('users_index_options', '/users/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('reset_tv_options', '/reset/tv-shows/:tvid', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('reset_users_options', '/reset/users/:uid', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))
    dispatcher.connect('reset_options', '/reset/', controller=optionsController, action='OPTIONS', conditions=dict(method=['OPTIONS']))

    conf = {
               'global' : {
                   'server.thread_pool' : 5,
                   'server.socket_host' : 'localhost',
                   'server.socket_port' : 51080,
               },
               '/': {
                   'request.dispatch' : dispatcher,
                   'tools.CORS.on': True,
               }
           }

    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    start_service()
