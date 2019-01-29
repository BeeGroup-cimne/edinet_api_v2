billing_amon_measures = {
    'resource_methods': ['POST'],
    'item_methods': [],
    'doc': {
            'body':
            """
            <p>billing_amon_measures is a "virtual" resource. In order to save memory we will decompose this document in 2 simpler ones.</p>
            <ul>
                <li>readings (used internally)</li>
                <li>billing_amon_measures_measurements (see resource documentation)</li>
            </ul>
            <p>
                We cannot retrieve billing_amon_measures items (or modify/delete).
                To delete error billing_amon_measures POST we should delete billing_amon_measures_measurements items (see resource documentation)
            </p>

            <h6>Resource example</h6>
            <pre>
{
  "measurements": 
  [
    {
      "timestamp_start_bill": "2013-10-11T00:00:00Z", 
      "timestamp_end_bill": "2013-11-11T00:00:00Z", 
      "type": "electricityConsumption", 
      "values": {
          "p1": 11.0,
          "p2": 9.1,
          "p3": 8.7
      }
    },
    {
      "timestamp_start_bill": "2013-10-11T00:00:00Z", 
      "timestamp_end_bill": "2013-11-11T00:00:00Z",      
      "type": "electricityKiloVoltAmpHours", 
      "values": {
          "p1": 11.0,
          "p2": 9.1,
          "p3": 8.7
      }
    },
    {
      "timestamp_start_bill": "2013-10-11T00:00:00Z", 
      "timestamp_end_bill": "2013-11-11T00:00:00Z",
      "type": "power", 
      "values": {
          "p1": 11.0,
          "p2": 9.1,
          "p3": 8.7
      }
    }
  ], 
  "readings": 
  [
    {"type": "electricityConsumption", "unit": "kWh"}, 
    {"type": "electricityKiloVoltAmpHours", "unit": "kVArh"},
    {"type": "power", "unit": "kW"}
  ], 
  "deviceId": "c1810810-0381-012d-25a8-0017f2cd3574"
}            
            </pre>
            """,
            'title':'billing_amon_measures help',
            },
    'schema': {
        'deviceId': {
            'type': 'string',
            'required': True,
        },
        'readings': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'type': {
                        'type':'string',
                        'required': True
                    },
                    'unit': {
                        'type': 'string',
                    },
                    'resolution': {
                        'type': 'float',
                    },
                    'accuracy': {
                        'type': 'float',
                    },
                    'min': {
                        'type': 'float',
                    },
                    'max': {
                        'type': 'float',
                    },
                    'correction': {
                        'type': 'boolean',
                    },
                    'correctedUnit': {
                        'type': 'string',
                    },
                    'correctionFactor': {
                        'type': 'float',
                    },
                    'correctionFactorBreakdown': {
                        'type': 'string',
                    },
                },
            },
        },
        'measurements': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'type': {
                        'type':'string',
                        'required': True
                    },
                    'timestamp_start_bill': {
                        'type': 'datetime',
                        'required': True,
                    },
                    'timestamp_end_bill': {
                        'type': 'datetime',
                        'required': True,
                    },
                    'values': {
                        'type': 'dict',
                        'required': True,
                        'schema': {
                            'p1': {
                                'type': 'float',
                                'required': False
                            },
                            'p2': {
                                'type': 'float',
                                'required': False
                            },
                            'p3': {
                                'type': 'float',
                                'required': False
                            },
                            'p4': {
                                'type': 'float',
                                'required': False
                            },
                            'p5': {
                                'type': 'float',
                                'required': False
                            },
                            'p6': {
                                'type': 'float',
                                'required': False
                            },
                        },
                    },
                    'error': {
                        'type': 'datetime',
                    },
                    'aggregated': {
                        'type': 'boolean'
                    },
                },
            },
        },
    },
}

billing_amon_measures_measurements = {
                    'resource_methods': ['DELETE','GET'],
                    'item_methods': [],
                    'allow_unknown': True,
                    'doc': {
                        'body':
                        """
                        <p>billing_amon_measures_measurements is an internal resource created on a billing_amon_measures POST. It has a field with a relation with readings, which indicates measures setup</p>
                        <p>Only method allowed is DELETE and GET. This is because an utility can't POST items relations. To correct some measures we should DELETE them and POST amon_measures again</p>
                        <p>When deleting items measures, all uploaded measures will be deleted </p>
                        """,
                        'title':'billing amon measures measurements help',
                    },
                    'schema': {
                        'deviceId': {
                            'type': 'string',
                            'required': True,
                        },
                        **billing_amon_measures['schema']['measurements']['schema']['schema']
                    }
}
