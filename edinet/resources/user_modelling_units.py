
user_modelling_units = {
    'item_lookup_field': 'userModellingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'league_table',
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'extra_response_fields': ['userModellingUnitId'],
    'doc': {
            'body':
            """
            <p>user_modelling_units resource to edit user_modelling_units information</p>
            <ul>
                <li>userModellingUnitId: Required. Unique Id used for identify each result</li>
                <li>buildings: Required. List of the modellingUnitId that must be included in results</li>
            </ul>
            <h6>Resource example</h6>
            <pre>
                    {
                      "userModellingUnitId": "userModellingUnitId-123",
                      "buildings": ["modellingUnitId-123", "modellingUnitId-234"]
                    }
            </pre>
            """,
            'title':'league_table help',
            },
    'schema' : {
        'userModellingUnitId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'buildings': {
             'type' : 'list',
             'required' : True
        }
    }
 }
