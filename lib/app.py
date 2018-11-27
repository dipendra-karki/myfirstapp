from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
from json import dumps

from user import User
from user_api import UserApi
from db import Db
from psycopg2 import sql
import logging
logging.basicConfig(level=logging.DEBUG)

class Router(object):

    @staticmethod
    def home_page(req):
        return req.render('index')



routes = [

    Rule('/', endpoint=Router.home_page),

    Rule('/api/cars', endpoint=UserApi.query, methods=['GET']),
    Rule('/api/cars', endpoint=UserApi.create, methods=['POST']),
    Rule('/api/cars/search', endpoint=UserApi.search, methods=['POST']),
    Rule('/api/cars/<id>', endpoint=UserApi.findById, methods=['GET']),
    Rule('/api/cars/<id>', endpoint=UserApi.update, methods=['PUT']),
    Rule('/api/cars/<id>', endpoint=UserApi.remove, methods=['DELETE']),
    
]

class App(object):
    def __init__(self, config):
        self.config = config
        self.url_map = Map(routes)
        self.jinja_env = Environment(
                loader=FileSystemLoader(config['template_path']),
                autoescape=True
            )

        Db.connect(config['db'])

    def render_template(self, template_name, **kwargs):
        tpl = self.jinja_env.get_template(template_name + '.html')
        return Response(tpl.render(kwargs), mimetype='text/html')

    def dispatch_request(self, req):
        adapter = self.url_map.bind_to_environ(req.environ)

        try:
            endpoint, values = adapter.match()
            req.params = values
            return endpoint(req)
        except NotFound as e:
            if req.headers['accept'] == 'application/json':
                return Response(
                    dumps({
                        'message': e.description,
                        'code': NotFound.code,
                    }),
                    mimetype='application/json',
                    status=NotFound.code
                )
            else:
                return e
        except BadRequest as e:
            if req.headers['accept'] == 'application/json':
                return Response(
                    dumps({
                        'message': e.description,
                        'code': BadRequest.code,
                    }),
                    mimetype='application/json',
                    status=BadRequest.code
                )
            else:
                return e
        except HTTPException, e:
            return e
    
    def wsgi_app(self, environ, start_response):
        req = Request(environ)
        req.render = self.render_template
        res = self.dispatch_request(req)
        return res(environ, start_response)

    def __call__(self, *args):
        return self.wsgi_app(*args)

