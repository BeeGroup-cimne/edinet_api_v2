from eve.utils import api_prefix
from flask_bootstrap import Bootstrap


class BaseHook(object):
    @staticmethod
    def set_hooks(app):
        raise NotImplementedError("Implemented in subclasses")

def set_hooks(app):
    for hook in app.config['HOOKS']:
        hook.set_hooks(app)

def set_docs(app):
    if app.config['DOCS']:
        Bootstrap(app)
        eve_docs = app.config['DOCS']()
        app.register_blueprint(eve_docs)

def set_methods(app):
    for method in app.config['METHODS']:
        prefix = api_prefix(api_version=app.config['API_VERSION'])
        app.register_blueprint(method, url_prefix=prefix)
