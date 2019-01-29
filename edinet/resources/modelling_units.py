modelling_units = {
    'item_lookup_field': 'modellingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'entity',
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'extra_response_fields': ['entityId'],
    'doc': {
        'body':
            """
            <p>@TODO: Modelling units docs.</p>

            <h6>Resource example</h6>
            <pre>
{
  "modellingUnitId": "Id-123",
  "label": "total without air conditioning",
  "location" : {
        "postalCode": "LE1",
        "countryCode": "GB"
    },
  "baseline": {
        "model": "Weekly30Min",
        "start": "2015-01-01T00:00:00Z",
        "end": "2016-01-01T00:00:00Z"
    },
  "devices": [
    {
      "deviceId": "c1810810-0381-012d-25a8-0017f2cd3574",
      "multiplier": 1.0
    },
    {
      "deviceId": "c1810810-0381-012d-25a8-0017f2cd3575",
      "multiplier": -1.0
      "replacementDate": "2017-01-01T00:00:00Z",
      "replacementDeviceId": "c1810810-0381-012d-25a8-0017f2cd3576"
    },
    {
      "deviceId": "c1810810-0381-012d-25a8-0017f2cd3576",
      "multiplier": -1.0
    }
  ],
  "energyType": "electricityConsumption"
}



            </pre>



            """,
        'title': 'modelling unit help',
    },
    'schema': {
        'modellingUnitId': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'label': {
            'type': 'string',
        },
        'location': {
            'type': 'dict',
            'schema': {
                'postalCode': {
                    'type': 'string'
                },
                'countryCode': {
                    'type': 'string',
                    'allowed': ['ES', 'IT', 'AT', 'FR', 'GB', 'DE', 'MT', 'GR', 'HR', 'EC']
                }
            }
        },
        'baseline': {
            'type': 'dict',
            'schema': {
                'start': {
                    'type': 'datetime'
                },
                'end': {
                    'type': 'datetime'
                },
                'model': {
                    'type': 'string',
                    'allowed': ['Weekly30Min', 'Weekly60Min', 'Monthly']
                }
            }
        },
        'devices': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'deviceId': {
                        'type': 'string',
                        'required': True,
                    },
                    'multiplier': {
                        'type': 'float',
                        'required': True
                    },
                    'replacementDate': {
                        'type': 'datetime'
                    },
                    'replacementDeviceId': {
                        'type': 'string'
                    }
                }
            }
        },
        'energyType': {
            'type': 'string',
            'allowed': ['electricityConsumption', 'gasConsumption', 'waterConsumption', 'heatConsumption']
        }
    }
}