from werkzeug.wrappers import Response
from werkzeug.wsgi import SharedDataMiddleware
from lib.app import App
from os import path

def create_app(config):
    app = App(config)

    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/public': config['public_path']
    })

    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    config = {
        'db': {
            'host': 'localhost',
            'user': 'dipendra',
            'password': 'postgres',
            'dbname': 'project',
        },
        'public_path': path.join(path.dirname(__file__), 'public'),
        'template_path': path.join(path.dirname(__file__), 'views'),
    }

    app = create_app(config)
    run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
