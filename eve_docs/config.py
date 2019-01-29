import json

from flask import current_app as capp
from eve.utils import home_link
from .labels import LABELS
from flask import Flask
import re
#Get resources by blueprint
def get_custom_functions(blueprint):
    temp_app = Flask(__name__)
    temp_app.register_blueprint(blueprint)
    ret = {}
    import_name = blueprint.__dict__['import_name']
    module_imported = __import__(import_name, fromlist=[''])
    functions_names = [x for x in dir(module_imported) if re.match("^api", x)]
    functions = {}
    for f in functions_names:
        functions[f]=module_imported.__dict__[f]
    for resource in temp_app.url_map.iter_rules():
        if resource.endpoint == 'static':
            continue
        endpoint = resource.endpoint.split(".")[1]
        function = functions[endpoint]
        try:
            function_doc = json.loads(re.sub('[\n\t]', '', function.__doc__)) if function.__doc__ else {"doc":{"title":"","body":""}}
        except:
            raise Exception("Invalid docstring for function{}".format(function))
        endpoint = endpoint.replace("api_","")
        func_call = str(resource).replace('<','{').replace('>','}')
        ret[endpoint] = {}
        ret[endpoint][func_call]={}
        ret[endpoint]["{}/no".format(func_call)]={}
        ret[endpoint]["doc"] = function_doc['doc']
        for method in resource.methods - set(list(['OPTIONS','HEAD'])):
            if method in function_doc:
                params = function_doc[method]["params"] if "params" in function_doc[method] else []
                label = function_doc[method]["label"] if "label" in function_doc[method] else get_custom_labels(endpoint, method)
            else:
                params = []
                label = get_custom_labels(endpoint, method)
            if not params:
                for argument in resource.arguments:
                    params.append({'name':argument, 'type':'string', 'required': True})
            ret[endpoint][func_call][method] = {
                'label': label,
                'params': params,
            }

    return ret

def get_cfg(blueprints):
    cfg = {}
    protocol = capp.config['PREFERRED_URL_SCHEME']
    home = home_link()
    cfg['base'] = '{}://{}'.format(protocol, home['href'])
    cfg['domains'] = {}
    cfg['server_name'] = capp.config['SERVER_NAME']
    cfg['api_name'] = capp.config.get('API_NAME', 'API')
    for domain in capp.config['DOMAIN'].keys():
        # empowering doc
        # added show_on_doc property where there aren't any item_methods nor resource_methods
        if capp.config['DOMAIN'][domain]['item_methods'] or capp.config['DOMAIN'][domain]['resource_methods'] or 'show_on_doc' in capp.config['DOMAIN'][domain]:
            cfg['domains'][domain] = {}
            cfg['domains'][domain] = paths(domain)
            if 'doc' in capp.config['DOMAIN'][domain]:
                cfg['domains'][domain]['doc'] = capp.config['DOMAIN'][domain]['doc']
    for b in blueprints:
        resources = get_custom_functions(b)
        for domain in resources:
            cfg['domains'][domain] = resources[domain]
    return cfg


def identifier(domain):
    name = capp.config['DOMAIN'][domain]['item_lookup_field']
    ret = {
        'name': name,
        'type': 'string',
        'required': True,
    }
    return ret


def schema(domain, field=None):
    ret = []
    if field is not None:
        params = {field: capp.config['DOMAIN'][domain]['schema'][field]}
    else:
        params = capp.config['DOMAIN'][domain]['schema']
    for field, attrs in params.items():
        template = {
            'name': field,
            'type': 'None',
            'required': False,
        }
        template.update(attrs)
        ret.append(template)
    return ret


def paths(domain):
    ret = {}
    path = '/{}'.format(domain)
    pathtype = 'resource'
    ret[path] = methods(domain, pathtype)

    primary = identifier(domain)
    path = '/{}/{}'.format(domain, pathparam(primary['name']))
    pathtype = 'item'
    ret[path] = methods(domain, pathtype)

    alt = capp.config['DOMAIN'][domain].get('additional_lookup', None)
    if alt is not None:
        path = '/{}/{}'.format(domain, pathparam(alt['field']))
        pathtype = 'additional_lookup'
        ret[path] = methods(domain, pathtype, alt['field'])
    return ret


def methods(domain, pathtype, param=None):
    ret = {}
    if pathtype == 'additional_lookup':
        method = 'GET'
        ret[method] = {}
        ret[method]['label'] = get_label(domain, pathtype, method)
        ret[method]['params'] = schema(domain, param)
    else:
        key = '{}_methods'.format(pathtype)
        methods = capp.config['DOMAIN'][domain][key]
        for method in methods:
            ret[method] = {}
            ret[method]['label'] = get_label(domain, pathtype, method)
            ret[method]['params'] = []
            if method == 'POST':
                ret[method]['params'].extend(schema(domain))
            elif method == 'PATCH':
                ret[method]['params'].extend(schema(domain))
                ret[method]['params'].append(identifier(domain))
            else:
                ret[method]['params'].append(identifier(domain))
    return ret


def pathparam(param):
    return '{{{}}}'.format(param)


def get_custom_labels(name, method):
    verb = LABELS[method]
    return '{} {}'.format(verb, name)

def get_label(domain, pathtype, method):
    verb = LABELS[method]
    if method == 'POST' or pathtype != 'resource':
        noun = capp.config['DOMAIN'][domain]['item_title']
        article = 'a'
    else:
        noun = domain
        article = 'all'
    return '{} {} {}'.format(verb, article, noun)
