monthly_aggregation = {
    'item_lookup_field': 'modellingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'monthly_aggregation',
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
    'doc': {
        'body':
        """
        <p>Monthly average consumption. The main fields are the following:</p>
            <ul>
                <li>modellingUnitId: modelling unit Id </li>
                <li>numberMonths: number of month of the consumption values considered in the calculation </li>
                <li>df: the records of the dataframe with aggregated consumption. It contains the following fields:</li>
                    <ul>
                        <li>value: the average value for m^2</li>
                        <li>days: the days considered in the calculations </li>
                        <li>ts: the timestamp of the row </li>
                     </ul>
            </ul>
            <h6>Resource example</h6>
            <pre>
            {
                "modellingUnitId": "modellingUnitId-123",              

                "df" : [ 
                    {
                        "days" : 29,
                        "value" : 6.053840063341255,
                        "ts" : datetime
                    },
                   {
                         "days" : 29,
                        "value" : 6.053840063341255,
                        "ts" : datetime
                    }
                ]  
            }

        </pre>
        """,
        'title':'edinet monthly aggregation',
    },
    'schema' : {
        'modellingUnitId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'df': {
            'type': 'list'
        },
        "anual_month" : {
            'type': 'float',
        },
        "anual_value" : {
            'type': 'float',
        },
    }
}