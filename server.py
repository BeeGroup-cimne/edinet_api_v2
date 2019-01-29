from time import strptime
import sys
from eve import Eve
from eve.io.mongo import Validator
from eve.utils import api_prefix
from auth.authentication import EVETokenAuth
from base_hooks import set_hooks, set_docs, set_methods


class EmpoweringValidator(Validator):
    # def _validate_type_string(self, field, value):
    #     # \s == the special re sequence '\s' matches Unicode whitespace characters including [ \t\n\r\f\v]
    #     if re.sub('[\r\n\t]', '', value) != value:
    #         self._error(field, "Field %s contains special characters: %s" % (field, re.sub('[\r\n\t]', '', value)))

    # def _validate_type_companyid(self, field, value):
    #     if not companies_cache.get(value):
    #         companies_cache.rebuild()
    #         if not companies_cache.get(value):
    #             self._error(field, "companyId field does not exist: %s" % value)

    def _validate_type_hour(self, field, value):
        try:
            strptime(value, "%H:%M:%S")
        except ValueError:
            self._error(field, "Field %s is not valid: %s. Expected format: hh:mm:ss" % (field, value))

    def _validate_type_month(self, field, value):
        try:
            strptime(value, "%m-%d")
        except ValueError:
            self._error(field, "Field %s is not valid: %s. Expected format: MM-DD" % (field, value))


app = Eve(validator=EmpoweringValidator, auth=EVETokenAuth)
set_hooks(app)
set_methods(app)
set_docs(app)
prefix = api_prefix(api_version=app.config['API_VERSION'])



if __name__ == '__main__':
    app.run()
