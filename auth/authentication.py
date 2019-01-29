from functools import wraps

from eve.auth import TokenAuth
from flask import current_app as app, request


class EVETokenAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        # use Eve's own db driver; no additional connections/resources are used
        companies = app.data.driver.db['companies']
        user_x = companies.find_one({'token': token})
        if user_x:
            self.set_request_auth_value(user_x['companyId'])
        return user_x


# def requires_auth(authenticated=False):
#     """
#     Mark a view method to require authentication and authorization. It will use
#     the auth configured in Eve.
#     Example::
#
#         @app.route('/')
#         @requires_auth("rest")
#         def myview():
#             pass
#     :param authenticated: By default False, if set to true, the view will be
#         executed if the user is authenticated
#     :rtype: The original funcion decorated.
#     """
#     def decorator_func(original):
#         @wraps(original)
#         def decorated(*args, **kwargs):
#             if authenticated:
#                 return original(*args, **kwargs)
#             accounts = app.data.driver.db['users']
#             auth_header = request.headers.get('Authorization')
#             token = auth_header.split(" ")[1]
#             user_x = accounts.find_one({'token': token})
#             if user_x:
#                 return original(*args, companyId=user_x['companyId'], **kwargs)
#         return decorated
#     return decorator_func