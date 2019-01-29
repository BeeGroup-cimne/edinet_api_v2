metering_amon_measures = {
    'resource_methods': ['POST'],
    'item_methods': [],
    'doc': {
            'body':
            """
            <p>metering_amon_measures is a "virtual" resource. In order to save memory we will decompose this document in 2 simpler ones.</p>
            <ul>
                <li>readings (used internally)</li>
                <li>metering_amon_measures_measurements (see resource documentation)</li>
            </ul>
            <p>
                We cannot retrieve metering_amon_measures items (or modify/delete).
                To delete error metering_amon_measures POST we should delete metering_amon_measures_measurements items (see resource documentation)
            </p>
        
            
            
            <h6>Resource example</h6>
            <pre>
{
  "measurements": 
  [
    {
      "timestamp": "2013-10-11T16:37:05Z", 
      "type": "electricityConsumption", 
      "value": 7.0
    },
    {
      "timestamp": "2013-10-11T16:37:05Z", 
      "type": "electricityKiloVoltAmpHours", 
      "value": 11.0
    }
  ], 
  "readings": 
  [
    {"type": "electricityConsumption", "period": "INSTANT", "unit": "kWh"}, 
    {"type": "electricityKiloVoltAmpHours", "period": "INSTANT", "unit": "kVArh"}
  ], 
  "deviceId": "c1810810-0381-012d-25a8-0017f2cd3574"
}            
            </pre>
            """,
            'title':'amon_measures help',
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
                    'period': { 
                        'type' : 'string',
                        'required': True,
                        'allowed' : [ 
                            'INSTANT', 
                            'CUMULATIVE',
                            ]
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
                    'timestamp': {
                        'type': 'datetime',
                        'required': True,
                    },
                    'value': {
                        'type': 'float',
                        'required': True,
                    },
                    'error': {
                        'type': 'datetime',
                        #'required': True,
                    },
                    'aggregated': {
                        'type': 'boolean'
                    },
                },
            },
        },
    },
}

metering_amon_measures_measurements = {
                    'resource_methods': ['DELETE','GET'],
                    'item_methods': [],
                    'allow_unknown': True,
                    'doc': {
                        'body':
                        """
                        <p>metering_amon_measures_measurements is an internal resource created on a metering_amon_measures POST. It has a field with a relation with readings, which indicates measures setup</p>
                        <p>Only method allowed is DELETE. This is because an utility can't POST items relations. To correct some measures we should DELETE them and POST metering_amon_measures again</p>
                        <p>When deleting items measures, all uploaded measures will be deleted </p>
                        """,
                        'title':'metering amon measures measurements help',
                    },   
                    'schema': {
                        'deviceId': {
                            'type': 'string',
                            'required': True,
                        },
                        **metering_amon_measures['schema']['measurements']['schema']['schema']
                    }
}
