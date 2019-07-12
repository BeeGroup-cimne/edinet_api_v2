from edinet.resources import companies, entities, buildings, league_table, reporting_units, \
    edinet_baseline, postal_codes, delete_measures, user_modelling_units, modelling_units, raw_data, \
    billing_amon_measures, metering_amon_measures, monthly_aggregation, benchmarking

DOMAIN = {
    'companies': companies.companies,
    'entities': entities.entities,
    'buildings': buildings.buildings,
    'modelling_units': modelling_units.modelling_units,
    'league_table': league_table.league_table,
    'reporting_units': reporting_units.reporting_units,
    'user_modelling_units': user_modelling_units.user_modelling_units,
    'postal_code': postal_codes.postal_codes,
    # amon related
    'metering_amon_measures': metering_amon_measures.metering_amon_measures,
    'metering_amon_measures_measurements': metering_amon_measures.metering_amon_measures_measurements,
    #'amon_measures_readings': amon_measures.amon_measures_readings,
    'billing_amon_measures': billing_amon_measures.billing_amon_measures,
    'billing_amon_measures_measurements': billing_amon_measures.billing_amon_measures_measurements,
    'delete_measures': delete_measures.delete_measures,
    # EDInet outputs
    'raw_data': raw_data.raw_data,
    'baselines': edinet_baseline.edinet_baseline,
    'monthly_aggregation': monthly_aggregation.monthly_aggregation,
    'benchmarking': benchmarking.benchmarking
}