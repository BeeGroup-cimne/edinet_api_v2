postal_codes = {
    'item_lookup_field': 'countryCode',
    'item_url': 'regex("[\S]+")',
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'doc': {
            'body':
            """
            <p> obtain the list of postal codes available in a country</p>
            """,
            'title':'postal code help',
            },
    'schema': {        
        'countryCode': {
            'type': 'string'
        },
        'postalCodes': {
            'type': 'list'
        }
    }
}