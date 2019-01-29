edinet_similar_groups_best_criteria = {
    'item_lookup_field': 'modellingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'comparisons',
    'resource_methods': ['GET'],
    'item_methods': ['GET'],
#     'datasource': {
#         'projection': {'companyId': 0}
#     },
    'doc': {
        'body':
        """
        <p>Comparison between similars. This resource provide the best criteria from the list of possible criterias. The main fields are the following:</p>
            <ul>
                <li>modellingUnitId: modelling unit Id </li>
                <li>numberMonths: number of month of the consumption values considered in the calculation </li>
                <li>criteria: from the proposed criterias which one is the best selected criteria</li>
                <li>groupCriteria: the values of the best criteria for this modellingUnitId</li>
                <li>values: a dictionary with the consumption values for this modellingUnitId. This dictionary includes the following fields:</li>
                    <ul>
                        <li>rd: number of days with consumption values </li>
                        <li>td: total number of days of the month </li>
                        <li>m: month </li>
                        <li>v: monthly consumption </li>
                        <li>v_surf: monthly consumption per square meter </li>
                    </ul>
            </ul>
            <h6>Resource example</h6>
            <pre>
            {
                "modellingUnitId": "modellingUnitId-123",              
                "numberMonths" : 12,
                "criteria" : "entityId + useType",
                "groupCriteria" : "GENCAT + primary_care_center"
                "values" : [ 
                    {
                        "rd" : 29,
                        "td" : 29,
                        "v_surf" : 6.053840063341255,
                        "m" : 201602,
                        "v" : 7646.000000000005
                    },
                   {
                        "rd" : 31,
                        "td" : 31,
                        "v_surf" : 6.231195566112433,
                        "m" : 201603,
                        "v" : 7870.000000000003
                    }
                ]  
            }

        </pre>
        """,
        'title':'edinet similar groups best criteria help',
    },
    'schema' : {
        'modellingUnitId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'numberMonths': { 
            'type': 'integer',
        },
        'criteria': {
            'type': 'string'
        },
        'groupCriteria': {
            'type': 'string'
        },
        'results': {
            'type': 'dict'
        },
        'values': {
            'type': 'dict'
        }
    }
}