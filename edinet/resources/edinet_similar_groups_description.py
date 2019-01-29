edinet_similar_groups_description = {
    'item_lookup_field': 'modellingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'edinet_similar_groups_description',
    'resource_methods': ['GET'],
    'item_methods': [],
#     'datasource': {
#         'projection': {'companyId': 0}
#     },
    'doc': {
        'body':
        """
        <p>Comparison between similars. This resource provide the results of the distribution of the different values for each group criteria. The main fields are the following:</p>
            <ul>
            <ul>
                <li>criteria: one of the proposed criterias</li>
                <li>groupCriteria: values of this criteria</li>
                <li>numberCustomers: number of customers included in this groupCriteria</li>
                <li>month: month of the consumption values considered in the calculation</li>
                <li>type: type of the energy values considered in the calculation</li>
                <li>results: dictionary that includes the distribution of the different values to compare. These values are: 'v' consumption [kWh] and 'v_surf [kWh/m2]</li>

            </ul>
            <h6>Resource example</h6>
            <pre>
            {       
                "month" : 201612,
                "criteria" : "entityId + useType",
                "groupCriteria" : "GENCAT + primary_care_center",
                "numberCustomers" : 7,
                "type": "gasConsumption",
                "results" : {
                    "rawMonths" : {
                        "v_surf" : {
                            "p75" : null,
                            "p5" : null,
                            "p95" : null,
                            "p25" : null,
                            "mean" : null,
                            "p50" : null,
                            "sd" : null
                        },
                        "v" : {
                            "p75" : 15345.5,
                            "p5" : 7260.5,
                            "p95" : 17655.5,
                            "p25" : 9570.5,
                            "mean" : 12458,
                            "p50" : 12458,
                            "sd" : 8167.083
                        }
                    }
                }
            }

        </pre>
        """,
        'title':'edinet similar groups description help',
    },
    'schema' : {
        'results': {
            'type': 'dict'
        },
        'month': { 
            'type': 'integer'
        },
        'numberCustomers': { 
            'type': 'integer'
        },
        'criteria': {
            'type': 'string'
        },
        'type': {
            'type': 'string'
        },
        'groupCriteria': {
            'type': 'string'
        }
    }
}