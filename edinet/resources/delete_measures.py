delete_measures = {
    'item_title': 'delete_measures',
    # 'additional_lookup': {
    #    'url': '[\w]+',
    #    'field': 'contractId'
    # },
    'resource_methods': ['GET', 'POST'],
    'item_methods': [],
    'doc': {
        'body':
            """
            <p>This resource will be used to delete the raw_data and baselines associated to the provided deviceId and to delete the measures from our Long-Term DataBase</p>
            <p>Every new entry will remove all measures stored for a deviceId</p>
            <p><em>Note:</em> This action cannot be undone!</p>
            <p>
                DateTimes ts_from and ts_to are optional as measure type. Not specifying any of those parameters
                will cause on removing all measures for the given device.
            </p>
            <p>
                To know the status of this operation in the field 'report' we can obtain the following information:
                <ul>
                    <li>status: [true/false] information about the status of the measures in hbase [deleted/not deleted]</li>
                    <li>deleted_old_data_from_mongo: [true/false] information about the status of the raw_data and baseline [deleted/not deleted] </li>
            </ul>
            </p>
            <h6>Resource POST example</h6>
            <pre>
{
    "deviceId": "111222333",
    "ts_from": ISODate("2015-02-01T01:00:00Z"),
    "ts_to": ISODate("2015-04-01T01:59:59Z"),
    "type": "electricityConsumption"
}
            </pre>

            <h6>Resource GET example</h6>
            <pre>
{
    "deviceId": "111222333",
    "ts_from": ISODate("2015-02-01T01:00:00Z"),
    "ts_to": ISODate("2015-04-01T01:59:59Z"),
    "type": "electricityConsumption",
    "report": {
        "status" : true,
        "finished_at" : ISODate("2017-04-13T03:19:48.818Z"),
        "started_at" : ISODate("2017-04-13T03:00:02.234Z"),
        "deleted_old_data_from_mongo" : true
    }
}
            </pre>

            """,
        'title': 'delete_measures help',
    },
    'schema': {
        'deviceId': {
            'type': 'string',
            'required': True,
        },
        'ts_from': {
            'type': 'datetime',
            'nullable': True
        },
        'ts_to': {
            'type': 'datetime',
            'nullable': True
        },
        "report": {
            'type': 'schema'
        },
    }
}