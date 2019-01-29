# flask imports
from datetime import datetime

from eve.auth import requires_auth
from eve.render import send_response
from flask import request, abort, Blueprint, g, Response
from flask import current_app as app

# utils imports
import numpy as np
import pandas as pd

from auth.authentication import EVETokenAuth

edinet_methods = Blueprint('edinet_methods', __name__)

"""
EVE docs has been modified to add desired blueprints function to the "API DOC". To use it: 
1. The method's name must start with "api_"
2. Docstring to the function with the json:
    { 
        "doc": {
            "title": "title",
            "body": "body",
        },
        #for each method i.e GET (optional, if not provided, default from the function signature will be used)
        "GET": {
            "label": "information of GET method",
            "params" [{"name": "first_param", "type": "type", "required":"false", "doc":"aditional_info", "**kwargs": "more_inofo"},..]
        }
    }
"""

@edinet_methods.route("/league_table_summarised/<leagueTableId>", methods=['GET'])
@requires_auth(EVETokenAuth)
def api_get_league_table_summarised(leagueTableId):
    """
    {
        "doc": {
            "title": "league table summarised help",
            "body": "<p> Obtain the sumarized of the league table </p>"
        },
        "GET": {
            "label": "Obtain the league_table sumarized",
            "params":[{"name": "leagueTableId", "type":"string", "required":"true", "doc":"id of the leage_table"},
                      {"name": "period", "type":"string", "required":"false", "info":"the period to sumarize", "values": ["D", "W", "M", "Y"]},
                      {"name": "type", "type":"list", "required":"false", "info":"the field to sumarize"}]
        }
    }
    """
    companyId = g.get("auth_value")
    # params from url
    period = request.args.get('period', 'M')
    type = request.args.get('type', ['savings', 'smileys'])
    if not isinstance(type, list):
        type = type.split(',')  # type=savings,smileys in the url

    periodsAllowed = ['D', 'W', 'M', 'Y']  # Weekly means Monday to Sunday
    period = period[0].upper()
    # recupero la info de mongo
    query = {'companyId': companyId, 'leagueTableId': leagueTableId}
    doc = app.data.driver.db['league_table'].find_one(query, {'_id': 0}, timeout=False)
    try:
        reporting_Units = doc['reporting_Units']
    except:
        reporting_Units = []

        # recupero la info de mongo de baseline i creo el resultat per cadascu
    res_report = {}
    for reportingUnit in reporting_Units:
        query_reporting = {'companyId': companyId, 'reportingUnitId': reportingUnit}
        doc_reporting = app.data.driver.db['reporting_units'].find_one(query_reporting, timeout=False)
        if doc_reporting:
            modelling_Units = doc_reporting['modelling_Units']
            res_report[reportingUnit] = []
            for modelUnit in modelling_Units:
                # update_baseline(companyId, modellingUnitId)   # TO DO
                query_baseline = {'companyId': companyId, 'modellingUnitId': modelUnit}
                doc_baseline = app.data.driver.db['baselines'].find_one(query_baseline,
                                                                        {'prediction': 1, 'values': 1, 'smileys': 1,
                                                                         'timestamps': 1}, timeout=False)
                if doc_baseline:
                    res_parcial = {}

                    # creo el dataframe
                    df = pd.DataFrame.from_records(
                        {'values': doc_baseline['values'], 'smileys': doc_baseline['smileys'],
                         'prediction': doc_baseline['prediction'], 'timestamps': doc_baseline['timestamps']})
                    df = df.set_index(pd.DatetimeIndex(df['timestamps']))
                    if df.empty != True and period in periodsAllowed:
                        for typ in type:
                            if typ in doc_baseline.keys() or typ == 'savings':
                                if typ in ['savings', 'values', 'prediction']:
                                    df_grouped = df.groupby(pd.TimeGrouper(freq=period)).sum()
                                else:
                                    df_grouped = df.groupby(pd.TimeGrouper(freq=period)).mean()

                                if typ == 'savings':
                                    res_parcial[typ] = df_grouped['prediction'] - df_grouped['values']
                                else:
                                    res_parcial[typ] = df_grouped[typ]
                                res_parcial[typ] = res_parcial[typ].where((pd.notnull(res_parcial[typ])),
                                                                          None).tolist()  # replacing nan by None
                            else:
                                res_parcial[typ] = None
                        try:  # if there is any valid type
                            res_parcial['modellingUnitId'] = modelUnit
                            res_parcial['timestamps'] = df_grouped.index.tolist()
                            res_parcial['number_of_elements'] = df['values'].groupby(
                                pd.TimeGrouper(freq=period)).count().tolist()
                        except:
                            for typ in type:
                                res_parcial[typ] = None
                            res_parcial['timestamps'] = None
                            res_parcial['number_of_elements'] = None
                            res_parcial['modellingUnitId'] = modelUnit

                    res_report[reportingUnit].append(res_parcial)

    return send_response('', (res_report, None, None, 200))


@edinet_methods.route("/reporting_unit_summarised/<reportingUnitId>", methods=['GET'])
@requires_auth(EVETokenAuth)
def api_get_reporting_unit_summarised(reportingUnitId):
    """
    {
        "doc": {
            "title": "reporting unit summarised help",
            "body": "<p> Obtain the sumarized of the reporting unit </p>"
        },
        "GET": {
            "label": "Obtain the reporting unit sumarized",
            "params":[{"name": "reportingUnitId", "type":"string", "required":"true", "doc":"id of the reporting_unit"},
                      {"name": "period", "type":"string", "required":"false", "info":"the period to sumarize", "values": ["D", "W", "M", "Y"]},
                      {"name": "type", "type":"list", "required":"false", "info":"the field to sumarize"}]
        }
    }
    """
    companyId = g.get("auth_value")
    # params from url
    period = request.args.get('period', 'M')
    type = request.args.get('type', ['savings', 'smileys'])
    if not isinstance(type, list):
        type = type.split(',')  # type=savings,smileys in the url

    periodsAllowed = ['D', 'W', 'M', 'Y']  # Weekly means Monday to Sunday
    period = period[0].upper()

    # recupero la info de mongo
    query_reporting = {'companyId': companyId, 'reportingUnitId': reportingUnitId}
    doc_reporting = app.data.driver.db['reporting_units'].find_one(query_reporting, timeout=False)
    res_report = []
    if doc_reporting:
        modelling_Units = doc_reporting['modelling_Units']
        for modelUnit in modelling_Units:
            # update_baseline(companyId, modellingUnitId)   # TO DO
            query_baseline = {'companyId': companyId, 'modellingUnitId': modelUnit}
            doc_baseline = app.data.driver.db['baselines'].find_one(query_baseline,
                                                                    {'prediction': 1, 'values': 1, 'smileys': 1,
                                                                     'timestamps': 1}, timeout=False)
            if doc_baseline:
                res_parcial = {}
                # creo el dataframe
                df = pd.DataFrame.from_records({'values': doc_baseline['values'], 'smileys': doc_baseline['smileys'],
                                                'prediction': doc_baseline['prediction'],
                                                'timestamps': doc_baseline['timestamps']})
                df = df.set_index(pd.DatetimeIndex(df['timestamps']))
                if df.empty != True and period in periodsAllowed:
                    for typ in type:
                        if typ in doc_baseline.keys() or typ == 'savings':
                            if typ in ['savings', 'values', 'prediction']:
                                df_grouped = df.groupby(pd.TimeGrouper(freq=period)).sum()
                            else:
                                df_grouped = df.groupby(pd.TimeGrouper(freq=period)).mean()

                            if typ == 'savings':
                                res_parcial[typ] = df_grouped['prediction'] - df_grouped['values']
                            else:
                                res_parcial[typ] = df_grouped[typ]
                            res_parcial[typ] = res_parcial[typ].where((pd.notnull(res_parcial[typ])),
                                                                      None).tolist()  # replacing nan by None
                        else:
                            res_parcial[typ] = None
                    try:  # if there is any valid type
                        res_parcial['modellingUnitId'] = modelUnit
                        res_parcial['timestamps'] = df_grouped.index.tolist()
                        res_parcial['number_of_elements'] = df['values'].groupby(
                            pd.TimeGrouper(freq=period)).count().tolist()
                    except:
                        for typ in type:
                            res_parcial[typ] = None
                        res_parcial['timestamps'] = None
                        res_parcial['number_of_elements'] = None
                        res_parcial['modellingUnitId'] = modelUnit

                res_report.append(res_parcial)

    return send_response('', (res_report, None, None, 200))



@edinet_methods.route("/modelling_unit_summarised/<modellingUnitId>", methods=["GET"])
@requires_auth(EVETokenAuth)
def api_modelling_unit_summarised(modellingUnitId):
    """
    {
        "doc": {
            "title": "modelling unit summarised help",
            "body": "<p> Obtain the sumarized of the modelling unit </p>"
        },
        "GET": {
            "label": "Obtain the modelling unit sumarized",
            "params":[{"name": "modellingUnitId", "type":"string", "required":"true", "doc":"id of the modelling_unit"},
                      {"name": "period", "type":"string", "required":"false", "info":"the period to sumarize", "values": ["D", "W", "M", "Y"]},
                      {"name": "type", "type":"list", "required":"false", "info":"the field to sumarize"}]
        }
    }
    """
    companyId = g.get("auth_value")
    # params from url
    period = request.args.get('period', 'M')
    type = request.args.get('type', ['savings', 'smileys'])
    if not isinstance(type, list):
        type = type.split(',')  # type=savings,smileys in the url

    periodsAllowed = ['D', 'W', 'M', 'Y']  # Weekly means Monday to Sunday
    period = period[0].upper()

    modellingUnitIdList = modellingUnitId.split(';')
    res_final = []
    for modellingUnit in modellingUnitIdList:
        # recupero la info de mongo
        # update_baseline(companyId, modellingUnitId)   # TO DO
        query_baseline = {'companyId': companyId, 'modellingUnitId': modellingUnit}
        query_fields = {'values': 1, 'prediction': 1, 'smileys': 1, 'timestamps': 1}
        doc_baseline = app.data.driver.db['baselines'].find_one(query_baseline, query_fields)
        res = {}

        if doc_baseline and 'values' in doc_baseline:
            n = -12 * 7 * 24 * 2
            # creo el dataframe
            df = pd.DataFrame.from_records({
                'values': doc_baseline['values'][n:],
                'smileys': doc_baseline['smileys'][n:],
                'prediction': doc_baseline['prediction'][n:],
                'timestamps': doc_baseline['timestamps'][n:]
            })
            df = df.set_index(pd.DatetimeIndex(df['timestamps']))
            df = df.drop('timestamps', 1)
            # a list is needed
            if not isinstance(type, list):
                type = [type]
            if df.empty != True and period in periodsAllowed:
                # calculo les agrupacions dels diff valors
                for typ in type:
                    if typ in doc_baseline.keys() or typ == 'savings':
                        if typ in ['savings', 'values', 'prediction']:
                            # filtre per negatius
                            df_grouped = df.clip(lower=0)
                            # filtre per valors >>>
                            # df_grouped = df_grouped[np.abs(df_grouped.prediction-df_grouped.prediction.mean())<=(10*df_grouped.prediction.std())]
                            df_grouped = df_grouped.groupby(pd.TimeGrouper(freq=period)).sum()
                        else:
                            df_grouped = df.groupby(pd.TimeGrouper(freq=period)).mean()
                        # res_parcial['groupedValues'] = df_grouped['value'].tolist()
                        # res_parcial['groupedPrediction'] = df_grouped['prediction'].tolist()
                        if typ == 'savings':
                            res[typ] = df_grouped['prediction'] - df_grouped['values']
                        else:
                            res[typ] = df_grouped[typ]
                        res[typ] = res[typ].where((pd.notnull(res[typ])), None).tolist()  # replacing nan by None
                    else:
                        res[typ] = None
                try:  # if there is any valid type
                    res['timestamps'] = df_grouped.index.tolist()
                    res['number_of_elements'] = df['values'].groupby(
                        pd.TimeGrouper(freq=period)).count().dropna().tolist()
                except:
                    for typ in type:
                        res[typ] = None
                    res['timestamps'] = None
                    res['number_of_elements'] = None
            else:
                # res_parcial['groupedValues'] =  None
                # res_parcial['groupedPrediction'] = None
                for typ in type:
                    res[typ] = None
                res['timestamps'] = None
                res['number_of_elements'] = None

        res_final.append(res)

    # torno una llista o un element
    res = res_final[0] if len(res_final) < 2 else res_final

    return send_response('', (res, None, None, 200))


@edinet_methods.route("/user_modelling_units_results/<userModellingUnitId>/<period>/<divider>",
                          methods=["GET"])
@requires_auth(EVETokenAuth)
def api_get_user_modelling_units_results(userModellingUnitId, period, divider):
    """
    {
        "doc": {
            "title": "user modelling units results help",
            "body": "<p> Obtain the user modelling units results </p>"
        },
        "GET": {
            "label": "Obtain the user modelling units results",
            "params":[{"name": "userModellingUnitId", "type":"string", "required":"true", "doc":"id of the user modelling_unit"},
                      {"name": "period", "type":"string", "required":"false", "info":"the period to sumarize", "values": ["D", "W", "M", "Y"]},
                      {"name": "divider", "type":"string", "required":"false", "info":"the field to divide the information"}]
        }
    }
    """
    companyId = g.get("auth_value")
    ######## start code

    periodsAllowed = ['D', 'W', 'M', 'Y']  # Weekly means Monday to Sunday
    modelling_unit_types = ['electricityConsumption', 'gasConsumption']
    period = period[0].upper()
    # recupero la info de mongo
    query = {'companyId': companyId, 'userModellingUnitId': userModellingUnitId}
    doc = app.data.driver.db['user_modelling_units'].find_one(query, {'_id': 0})  # timeout=False)
    try:
        building_id = doc['buildings']
    except:
        building_id = []

    buildings_docs = []
    for i, building in enumerate(building_id):
        query_building = {'companyId': companyId, 'buildingId': building}
        doc_building = app.data.driver.db['buildings'].find_one(query_building, {'buildingId': 1, 'data.' + divider: 1})
        if doc_building:
            buildings_docs.append(doc_building)
            # need to clean the building to obtain the desired dictionary

    clean_building_docs = [
        {
            "buildingId": b['buildingId'],
            divider: b['data'][divider] if divider in b['data'] else 'unknown',
        }
        for b in buildings_docs
    ]

    # create the dataframe of buildings
    building_df = pd.DataFrame.from_records(clean_building_docs)
    # get all divider and group the tables, then filter them by the different groups
    building_divider_values = building_df[divider].unique()
    building_grouped = building_df.groupby(divider)
    # initialize the results variable
    results = {}
    # iterate for all modelling unit types
    for modelling_unit_type in modelling_unit_types:
        baselines_by_divider = pd.DataFrame()
        # and all different divider groups
        for building_divider in building_divider_values:
            # get the buildings of thes divider
            buildings_by_divider = building_grouped.get_group(building_divider)
            baselines_by_divider_temp = []
            for building_id in buildings_by_divider.buildingId:
                query_baseline = {'companyId': companyId, 'modellingUnitId': building_id + '-' + modelling_unit_type}
                doc_baseline = app.data.driver.db['baselines'].find_one(query_baseline,
                                                                        {'P50': 1, 'values': 1, 'timestamps': 1})
                if (doc_baseline):
                    if len(doc_baseline['values']) == len(doc_baseline['P50']) == len(doc_baseline['timestamps']):
                        df = pd.DataFrame.from_records({'values': doc_baseline['values'], 'P50': doc_baseline['P50'],
                                                        'timestamps': doc_baseline['timestamps']})
                        df = df.set_index(pd.DatetimeIndex(df['timestamps']))
                        df_grouped = df.groupby(pd.TimeGrouper(freq=period)).sum()
                        baselines_by_divider_temp.append(df_grouped)
            if baselines_by_divider_temp:
                baselines_by_divider_temp = pd.concat(baselines_by_divider_temp, axis=1)
                v = baselines_by_divider_temp  # dropna
                try:
                    final = pd.DataFrame.from_records({'P50': v['P50'].sum(axis=1), 'values': v['values'].sum(axis=1)})
                except:
                    final = v
            else:
                final = pd.DataFrame()
            final.rename(index=str, columns={'values': 'values-' + building_divider, 'P50': 'P50-' + building_divider},
                         inplace=True)
            # print(final.dropna())
            baselines_by_divider = pd.concat([baselines_by_divider, final.dropna()], axis=1)
            baselines_by_divider = baselines_by_divider

        results[modelling_unit_type] = {
            "timestamps": baselines_by_divider.index.tolist() if not v.empty else []
        }
        for divider in building_divider_values:
            try:
                results[modelling_unit_type].update({
                    divider: {
                        "values": baselines_by_divider['values-' + divider].tolist() if not v.empty else [],
                        "P50": baselines_by_divider['P50-' + divider].tolist() if not v.empty else []
                    }
                })
            except:
                pass

    return send_response('', (results, None, None, 200))


@edinet_methods.route("/v1/building_info/<CUPS>", methods=['GET'])
@requires_auth(EVETokenAuth)
def api_get_building_info(CUPS):
    """
    {
        "doc": {
            "title": "building info help",
            "body": "<p> Obtain the information of the building containing the cups </p>"
        },
        "GET": {
            "label": "Obtain the information of the building containing the cups",
            "params":[{"name": "CUPS", "type":"string", "required":"true", "doc":"the cups of the device"}]
        }
    }
    """
    companyId = g.get("auth_value")
    # recupero la info de mongo sobre el CUPS
    query = {"devices": {"$elemMatch": {"deviceId": CUPS}}}
    doc = app.data.driver.db['modelling_units'].find_one(query, {'_id': 0})
    res_report = None
    if doc:
        # recupero la info de mongo de buildings i creo el resultat
        buildingId = doc['modellingUnitId'].split('-')[0]
        # query = { "buildingId":buildingId, 'data.organizationLevel2': '1-salut' }
        query = {"buildingId": buildingId,
                 'entityId': {'$in': ['residencies-avis', 'generalitat-de-catalunya', 'gipuzkoako_foru_aldundia']}}
        res_report = app.data.driver.db['buildings'].find_one(query,
                                                              {'_id': 0, 'companyId': 0, '_etag': 0, '_created': 0})

    return send_response('', (res_report, None, None, 200))


# De moment no executo MRJobs des d'aqui
# @edinet_methods.route("/v1/recalculated_baseline/<modellingUnitId>", methods=['GET'])
# @requires_auth(EVETokenAuth)
# def get_recalculated_baseline(modellingUnitId):
#     companyId = g.get("auth_value")
#
#     # recupero la data de creacio del baseline
#     doc = app.data.driver.db['baselines'].find_one({'companyId': companyId, 'modellingUnitId': modellingUnitId},
#                                                    {'_created': 1})
#     created = doc['_created'] if doc and '_created' in doc else None
#     date_now = datetime.now().replace(microsecond=0)
#     if created:
#         created = created.replace(tzinfo=None)
#         diff = date_now - created
#         diff_hours = diff.seconds / 3600.0
#
#     # recalculo el baseline
#     if not created or diff_hours > 1:
#         res = update_baseline(companyId, modellingUnitId, updated=[True])
#
#     # recupero el baseline
#     query = {"companyId": companyId, 'modellingUnitId': modellingUnitId}
#     res_report = app.data.driver.db['baselines'].find_one(query, {'_id': 0, '_etag': 0, '_created': 0, 'P50_month': 0,
#                                                                   'values_month': 0, 'timestamps_month': 0},
#                                                           timeout=False)
#
#     return send_response('', (res_report, None, None, 200))
