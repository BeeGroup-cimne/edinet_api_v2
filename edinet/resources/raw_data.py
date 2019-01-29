raw_data = {
    'item_lookup_field': 'deviceId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'raw_data',
    'resource_methods': [],
    'item_methods': ['GET'],
#     'datasource': {
#         'projection': {'companyId': 0}
#     },
    'doc': {
        'body':
        """
        <p>Raw Data is ordered time series resource of the device. The main fields are the following:</p>
            <ul>
                <li>deviceId: Required. Id used for each utility internally</li>
                <li>timestamps: list of considered timestamps </li>
                <li>values: list of energy consumption values</li>
            </ul>
            <h6>Resource example</h6>
            <pre>
            {
                "deviceId": "deviceId-123",
                "timestamps" : [ "2014-01-01T00:00:00.000Z", "2014-01-01T00:30:00.000Z", ... , "2014-12-31T23:30:00.000Z"], 
                "values" : [ 0.59, 1, 0.11, 0.1, 0.1, 0.09, 0.08, 0.08, 0.09, 0.11, 0.14, ... , 0.14],
            },

        </pre>
        """,
        'title':'raw_data help',
    },
    'schema' : {
        'deviceId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'timestamps': {
            'type': 'schema'         
        },
        "values": {
             'type': 'schema'            
        }
    }
}