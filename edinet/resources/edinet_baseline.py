edinet_baseline = {
    'item_lookup_field': 'modellingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'baselines',
    'resource_methods': [],
    'item_methods': ['GET'],
#     'datasource': {
#         'projection': {'companyId': 0}
#     },
    'doc': {
        'body':
        """
        <p>Baseline is ordered time series resource of the modelling_unit. The main fields are the following:</p>
            <ul>
                <li>modellingUnitId: modelling unit Id </li>
                <li>timestamps: list of considered timestamps </li>
                <li>values: list of energy consumption values</li>
                <li>P5: list of the percentile 05 of the model residuals</li>
                <li>P25: list of the percentile 25 of the model residuals</li>
                <li>P75: list of the percentile 75 of the model residuals</li>
                <li>P95: list of the percentile 95 of the model residuals</li>
                <li>smileys: list of the percentileofscore of the given consumption</li>
                <li>prediction: list of the model prediction</li>
            </ul>
            <h6>Resource example</h6>
            <pre>
            {
                "modellingUnitId": "modellingUnitId-123",
                "timestamps" : [ "2014-01-01T00:00:00.000Z", "2014-01-01T00:30:00.000Z", ... , "2014-12-31T23:30:00.000Z"], 
                "values" : [ 0.59, 1, 0.11, 0.1, 0.1, 0.09, 0.08, 0.08, 0.09, 0.11, 0.14, ... , 0.14],
                "P5" : [ 0.5, 1, 0.1, 0.1, 0.1, 0.09, 0.08, 0.08, 0.09, 0.11, 0.14, ... , 0.14],
                "P25" : [ 0.5, 1, 0.1, 0.1, 0.1, 0.09, 0.08, 0.08, 0.09, 0.11, 0.14, ... , 0.14],
                "P75" : [ 0.5, 1, 0.1, 0.1, 0.1, 0.09, 0.08, 0.08, 0.09, 0.11, 0.14, ... , 0.14],
                "P95" : [ 0.5, 1, 0.1, 0.1, 0.1, 0.09, 0.08, 0.08, 0.09, 0.11, 0.14, ... , 0.14],
                "smileys": [80.0, 90.0, 50.0 , ... , 25.5],
                "prediction" : [ 0.5, 1, 0.1, 0.1, 0.1, 0.09, 0.08, 0.08, 0.09, 0.11, 0.14, ... , 0.14],
                "values_month": [ 200, 300, ... 33 ] # 12 values
                "P50_month": [" 14, 30 ,33, ... , 33] # 12 values
                "timestamps_month": [1,2,3,4 ]        
            }

        </pre>
        """,
        'title':'edinet baseline help',
    },
    'schema' : {
        'modellingUnitId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'timestamps': {
            'type': 'schema'         
        },
        "values": {
             'type': 'schema'            
        },
        "P5": {
             'type': 'schema'            
        },
        "P25": {
             'type': 'schema'            
        },
        "P50": {
             'type': 'schema'            
        },
        "P75": {
             'type': 'schema'            
        },
        "P95": {
             'type': 'schema'            
        },
        "temperatures": {
             'type': 'schema'            
        },
        "prediction": {
             'type': 'schema'            
        },
        "smileys": {
             'type': 'schema'            
        },
        "values_month": {
             'type': 'schema'
        },
        "P50_month": {
             'type': 'schema'
        },
        "timestamps_month": {
             'type': 'schema'
        }
    }
}