import os
from edinet import domain
from edinet.edinet_docs import edinet_docs
from edinet.edinet_hooks import MeasuresHooks, WeatherStationHooks
from edinet.edinet_methods import edinet_methods

HOOKS = [MeasuresHooks, WeatherStationHooks]

MEASURES_RESOURCES=['billing_amon_measures', 'metering_amon_measures']
POSTAL_CODE_FILE = os.environ['POSTAL_CODE_FILE']
DEFAULT_LATITUDE = "41.6167"
DEFAULT_LONGITUDE = "0.6222"
DEFAULT_ALTITUDE = "181.0"

DOCS = edinet_docs

METHODS = [edinet_methods]

MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = os.environ['MONGO_PORT']
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
MONGO_DBNAME = os.environ['MONGO_DBNAME']

if os.environ['SERVER_NAME']:
    SERVER_NAME = os.environ['SERVER_NAME']
URL_PROTOCOL = os.environ['URL_PROTOCOL']
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

API_VERSION = 'v1'
AUTH_FIELD = "companyId"
DOMAIN = domain.DOMAIN
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
