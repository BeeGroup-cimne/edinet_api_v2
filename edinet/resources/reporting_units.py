
reporting_units = {
    'item_lookup_field': 'reportingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'reporting_units',
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'extra_response_fields': ['reportingUnitId'],
    'doc': {
            'body':
            """
            <p>reporting_unit resource information</p>
            <ul>
                <li>reportingUnitId: Required. Unique Id used for identify each reporting_unit coming from edinet platform</li>
                <li>modelling_Units: Required. List of the modellingUnitId that are included in the reporting_unit</li>
                <li>buildingId: Id to identify the associated building</li>
                <li>typeList: list of types associated respectively to each modellingUnitId</li>
            </ul>
            <h6>Resource example</h6>
            <pre>
                    {
                      "reportingUnitId": "reportingUnitId-123",
                      "modelling_Units": ["modellingUnitId-123", "modellingUnitId-234"],
                      "buildingId": "buildingId-123",
                      "typeList": ["gasConsumption","waterConsumption"]
                    }
            </pre>
            """,
            'title':'reporting_units help',
            },
    'schema' : {
        'reportingUnitId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'modelling_Units': {
             'type' : 'list',
             'required' : True
        },
        'buildingId': {
             'type' : 'string'
        },
        'typeList': {
             'type' : 'list',
        }
    }
 }
