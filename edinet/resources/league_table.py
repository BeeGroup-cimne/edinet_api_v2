
league_table = {
    'item_lookup_field': 'leagueTableId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'league_table',
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'extra_response_fields': ['leagueTableId'],
    'doc': {
            'body':
            """
            <p>league_table resource to edit league table information</p>
            <ul>
                <li>leagueTableId: Required. Unique Id used for identify each league_table coming from edinet platform</li>
                <li>reporting_Units: Required. List of the reportingUnitId that must be included in the league table</li>
            </ul>
            <h6>Resource example</h6>
            <pre>
                    {
                      "leagueTableId": "leagueTableId-123",
                      "reporting_Units": ["reportingUnitId-123", "reportingUnitId-234"]
                    }
            </pre>
            """,
            'title':'league_table help',
            },
    'schema' : {
        'leagueTableId': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'reporting_Units': {
             'type' : 'list',
             'required' : True
        }
    }
 }
