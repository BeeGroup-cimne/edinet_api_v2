benchmarking = {
    'item_lookup_field': 'modellingUnitId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'benchmarking',
    'resource_methods': ['GET'],
    'item_methods': [],
    'doc': {
        'body':
        """
        <p>Comparison between similars. This resource provide the results of the distribution of the different values for each group criteria. The main fields are the following:</p>
            <ul>
            <ul>
                <li>criteria: one of the proposed criterias</li>
                <li>criteria_values: values of this criteria</li>
                <li>num_buildings: number of buildings included in this groupCriteria</li>
                <li>month: month of the consumption values considered in the calculation</li>
                <li>energyType: type of the energy values considered in the calculation</li>
                <li>quantile_*: the distribution depending on the quantiles indicated in the definition</li>

            </ul>
            <h6>Resource example</h6>
            <pre>
                {
                "_id" : ObjectId("5d25a1e93eb53b6cc6590c87"),
                "criteria" : "type",
                "quantile_50" : 0.97694105,
                "energyType" : "gasConsumption",
                "quantile_75" : 1.194185,
                "quantile_90" : 1.42819582,
                "month" : "01",
                "quantile_25" : 0.49949766,
                "quantile_5" : 0.1375924223,
                "criteria_values" : "residential"
                }
        </pre>
        """,
        'title':'benchmarking description help',
    },
    'allow_unknown': True,
    'schema' : {}
}