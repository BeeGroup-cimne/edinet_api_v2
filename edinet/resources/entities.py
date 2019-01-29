entities = {
    'item_lookup_field': 'entityId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'entity',
    'resource_methods': ['GET','POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'extra_response_fields': ['entityId'],
    'doc': {
        'body':
            """
            <p>@TODO: Entity docs.</p>
            """,
        'title': 'entity help',
    },
    'schema': {
        'entityId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'name': {
            'type': 'string',
        },
        'address': {
            'type': 'dict',
            'schema': {
                'city': { 'type' : 'string' },
                'cityCode': { 'type' : 'string' },
                'countryCode': { 'type' : 'string' },
                'country': { 'type' : 'string' },
                'street': { 'type' : 'string' },
                'postalCode': { 'type' : 'string' },
                'province': { 'type' : 'string' },
                'provinceCode': { 'type' : 'string' },
            },
        },
    }
}