# coding=utf-8

from flask import Flask, Blueprint
from flask.views import View

def add_router(main_app, route_map):
    '''

    add_router is helper function to merge api list to flask app

    first , create a flask app object

    >>> app = Flask(__name__)

    then , define a function returns somethings

    >>> def hello():
    >>> ... return 'Hello,World'

    and now , add hello function to api list , and call add_router with flask app and api_list

    >>> api_list = (('/', hello), )
    >>> add_router(app, api_list)

    try to run flask app , the browser will return "Hello,World"

    '''

    for url, slot_obj in route_map:
        if isinstance(slot_obj, Blueprint):
            main_app.register_blueprint(slot_obj, url_prefix=url)
        elif callable(slot_obj):
            main_app.add_url_rule(url, view_func=slot_obj)
        else:
            raise Exception('bad sub application item type')


class DummyClass(object):

    def __getattr__(self, item):
        raise Exception('please install python-socketio package to enable socket.io feature')

from flask.app import get_debug_flag
import logging

try:

    import socketio
    sio = socketio.Server(logger=get_debug_flag())

except:

    sio = DummyClass()


class FlaskSocketIO(Flask):

    def __init__(self):
        super().__init__(__name__)
        if not isinstance(sio, DummyClass):
            self.wsgi_app = socketio.Middleware(sio, self.wsgi_app)

    def run(self, host=None, port=None, debug=None,
            load_dotenv=True, **options):
        if not isinstance(sio, DummyClass):
            if sio.async_mode != 'threading':
                from engineio import async_threading
                sio.eio._async = async_threading._async
            if debug and (not get_debug_flag()):
                # sio not initialized with debug ,
                # try set logger level directly
                sio.logger.setLevel(logging.DEBUG)
        super().run(host, port, debug, load_dotenv, **options)



def build_app(sub_apis=()):
    main_app = FlaskSocketIO()
    for sub_api in sub_apis:
        if isinstance(sub_api, (tuple, list)):
            add_router(main_app, sub_api)
        elif hasattr(sub_api, 'route_map'):
            if isinstance(sub_api.route_map, (tuple, list)):
                add_router(main_app, sub_api.route_map)
            else:
                raise Exception('bad route map type')
        else:
            raise Exception('unknown app type')
    return main_app


