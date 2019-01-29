buildings = {
    'item_lookup_field': 'buildingId',
    'item_url': 'regex("[\S]+")',
    'item_title': 'building',
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],
    'extra_response_fields': ['buildingId'],
    'doc': {
        'body':
            """
            <p>Building is a composed document. It has its own fields and 5 subdocuments</p>
            <ul>
                <li>data: information about the buildings</li>
                <li>address: information relative to the building location</li>
                <li>profile: information relative to the description of the building use profile</li>
                <li>system: information about building facilities</li>
                <li>eem: information relative to Energy Efficiency Measures</li>
            </ul>
            <p>There are some important fields on Building that needs some review</p>
            <ul>
                <li>buildingId: Required. Unique Id of the building</li>
                <li>entityId: Required. Entity to which the building belongs</li>
            </ul>
            <h6>Resource example</h6>
            <pre>
{
  "buildingId": "buildingId-123",
  "entityId": "entityId-123",
  "address": {
      "city": "city-123",
      "cityCode": "cityCode-123",
      "countryCode": "ES",
      "country": "Spain",
      "street": "street-123",
      "postalCode": "postalCode-123",
      "province": "Barcelona",
      "provinceCode": "provinceCode-123",
      "parcelNumber": "parcelNumber-123"
    },
    "data": {
      "organizationLevel1": "level1",
      "organizationLevel2": "level2",
      "organizationLevel3": "level3",
      "constructionYear": 1990,
      "cadastreReference": "3XFRE34HJ56",
      "areaUtil": 90,
      "areaBuild": 100,
      "areaProperty": 200,
      "volume": 300,
      "type": "flat",
      "useType": "residential_single_house",
      "dwellingPositionInBuilding": "first_floor",        
      "buildingOrientation": "S",
      "weatherStation": "weatherStation-123"
    },
    "profile": {   
      "numberOfOccupants": 10,
      "profilePercentageOfOccupation": [0.5,1.0,0.25...]  # 24x7 float values
      "percentageDateStart": "2013-01-01T00:00:00Z",
      "percentageDateEnd": "2013-12-31T23:59:59Z",
      "profileOcupation": [1,0,0...] # 24x7 boolean values
      "ocupationDateStart": "2013-01-01T00:00:00Z",
      "ocupationDateEnd": "2013-12-31T23:59:59Z",
      "vacationDays":  ["2016-05-05T14:33:18Z","2016-05-05T14:33:18Z"]
    },
    "system": {
      "buildingWindowsType": "single_panel",
      "buildingWindowsFrame": "PVC",
      "buildingHeatingSource": "electricity",
      "buildingHeatingPower": 10000,
      "buildingCoolingSource": "electricity",
      "buildingCoolingPower": 5000,
      "buildingCoolHeatSameSyst" : 1,
      "buildingDHWSource": "electricity",
      "buildingDHWPower": 2000,
      "buildingDHWHeatSameSyst" : 0,
      "buildingSolarSystem": "PV",
      "buildingSolarPower": 10000,
      "buildingSolarArea": 10
    },
    "eem": 
      [ 
        {
          "eemType": "Heating",
          "eemSubsource": "Production",
          "eemSelected" : { "eemApplied": "",
                            "eemAppliedParam1": "",
                            "eemAppliedParam2": "",
                            "eemAppliedParam3": ""
                          },
          "eemInvestment" : { "investment": 20000,
                              "maintenance": 1000
                            },  
          "eemDate" : { "applicationDate": "2013-01-01T00:00:00Z",
                        "contractDate": "2013-01-01T00:00:00Z",
                        "installationDate": "2013-01-01T00:00:00Z"
                      },
          "eemAssessment" : { "satisfactionAssessment": "5",
                              "complexityAssessment": "5"
                            },
        },
        {
          "eemType": "Heating",
          "eemSubsource": "Production",
          "eemSelected" : { "eemApplied": "",
                            "eemAppliedParam1": "",
                            "eemAppliedParam2": "",
                            "eemAppliedParam3": ""
                          },
          "eemInvestment" : { "investment": 20000,
                              "maintenance": 1000
                            },  
          "eemDate" : { "applicationDate": "2013-01-01T00:00:00Z",
                        "contractDate": "2013-01-01T00:00:00Z",
                        "installationDate": "2013-01-01T00:00:00Z"
                      },
          "eemAssessment" : { "satisfactionAssessment": "8",
                              "complexityAssessment": "9"
                            },
        }
    ],
    "modellingUnits": [
                         modellingUnitId-123, modellingUnitId-1234
                      ],
    "hourlyData": True,
    "buildingName": "building_name"
    }

}
            </pre>
            """,
        'title': 'building help',
    },
    'schema': {
        'buildingId': {
            'type': 'string',
            'required': True,
            'unique': True
        },
        'entityId': {
            'type': 'string',
            'required': True
        },
        'address': {
            'type': 'dict',
            'schema': {
                'city': {'type': 'string'},
                'cityCode': {'type': 'string'},
                'countryCode': {'type': 'string'},
                'country': {'type': 'string'},
                'street': {'type': 'string'},
                'postalCode': {'type': 'string'},
                'province': {'type': 'string'},
                'provinceCode': {'type': 'string'},
                'parcelNumber': {'type': 'string'}
            },
        },
        'data': {
            'type': 'dict',
            'schema': {
                'organizationLevel1': {'type': 'string'},
                'organizationLevel2': {'type': 'string'},
                'organizationLevel3': {'type': 'string'},
                'constructionYear': {'type': 'integer'},
                'cadastreReference': {'type': 'string'},
                'areaUtil': {'type': 'integer'},
                'areaBuild': {'type': 'integer'},
                'areaProperty': {'type': 'integer'},
                'volume': {'type': 'integer'},
                'type': {'type': 'string',
                         'allowed': ['flat', 'detached', 'semi-detached_building', 'terraced_building', 'row_building',
                                     'tower_building', 'courtyard_building']
                         },
                'useType': {'type': 'string',
                            'allowed': ['residential', 'residential_single_house', 'residential_apartment_block',
                                        'residential_single_terrace', 'office_computer_center', 'office_police',
                                        'office_fire_brigade', 'office_technical_service', 'office_call_center',
                                        'office_public_attention', 'office', 'school', 'school_vocational',
                                        'school_kindergarten', 'school_higher', 'school_lecture_hall',
                                        'school_laboratory', 'school_library', 'hospital', 'hospital_surgery',
                                        'hospital_nursing', 'hospital_almshome', 'primary_care_center',
                                        'hospital_day_care', 'hostel', 'restaurant', 'sport', 'sports_center',
                                        'sports_hall', 'sport_swimming_pool', 'cultural', 'cultural_museum',
                                        'cultural_theater', 'cinema', 'market', 'commerce', 'garage', 'social_center',
                                        'social_center_elder', 'others', 'unknown', 'school_craft',
                                        'correctional_facility', 'supermarket', 'shopping_mall', 'swimming_pool',
                                        'fittness_swimming_pool', 'spa', 'fittness_centre', 'school_primary',
                                        'school_secondary', 'school_music', 'school_military', 'guesthouse',
                                        'hotel_1to3star', 'hotel_4to5star', 'bar_cafeteria', 'penitentiary_centre',
                                        'student_residence', 'geriatric_residence', 'warehouse']

                            },
                'dwellingPositionInBuilding': {'type': 'string',
                                               'allowed': ['first_floor', 'middle_floor', 'last_floor', 'other']
                                               },
                'buildingOrientation': {'type': 'string',
                                        'allowed': ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']
                                        },
                'weatherStation': {'type': 'string'}
            },
        },
        'profile': {
            'type': 'dict',
            'schema': {
                'numberOfOccupants': {'type': 'integer'},
                'percentageOfOccupation': {'type': 'list',
                                           'schema': {'type': 'float'},
                                           'minlength': 168,
                                           'maxlength': 168
                                           },
                'percentageDateStart': {'type': 'datetime'},
                'percentageDateEnd': {'type': 'datetime'},
                'profileOcupation': {'type': 'list',
                                     'schema': {'type': 'boolean'},
                                     'minlength': 168,
                                     'maxlength': 168
                                     },
                'ocupationDateStart': {'type': 'datetime'},
                'ocupationDateEnd': {'type': 'datetime'},
                'vacationDays': {'type': 'list',
                                 'schema': {'type': 'datetime'},
                                 }
            },
        },
        'system': {
            'type': 'dict',
            'schema': {
                'buildingWindowsType': {'type': 'string',
                                        'allowed': ['single_panel', 'double_panel', 'triple_panel', 'low_emittance',
                                                    'other']
                                        },
                'buildingWindowsFrame': {'type': 'string',
                                         'allowed': ['PVC', 'wood', 'aluminium', 'steel', 'other']
                                         },
                'buildingHeatingSource': {'type': 'string',
                                          'allowed': ['electricity', 'gas', 'gasoil', 'district_heating', 'biomass',
                                                      'other']
                                          },
                'buildingHeatingPower': {'type': 'integer'},
                'buildingCoolingSource': {'type': 'string',
                                          'allowed': ['electricity', 'district_heating', 'other']
                                          },
                'buildingCoolingPower': {'type': 'integer'},
                'buildingCoolHeatSameSyst': {'type': 'boolean'},
                'buildingDHWSource': {'type': 'string',
                                      'allowed': ['electricity', 'gas', 'gasoil', 'district_heating', 'biomass',
                                                  'other']
                                      },
                'buildingDHWPower': {'type': 'integer'},
                'buildingDHWHeatSameSyst': {'type': 'boolean'},
                'buildingSolarSystem': {'type': 'string',
                                        'allowed': ['PV', 'solar_themal_heating', 'solar_thermal_DHW', 'other']
                                        },
                'buildingSolarPower': {'type': 'integer'},
                'buildingSolarArea': {'type': 'integer'}
            },
        },
        'eem': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'eemType': {'type': 'string',
                                'allowed': ['Heating', 'Cooling', 'DHW', 'Lighting', 'Electric_Equipment', 'Envelop',
                                            'Management', 'Other']
                                },
                    'eemSubsource': {'type': 'string',
                                     'allowed': ['Production', 'Distribution', 'Final_elements', 'Storage',
                                                 'Control_regulation', 'Management', 'General', 'Other']
                                     },
                    'eemSelected': {'type': 'dict',
                                    'schema': {
                                        'eemApplied': {'type': 'string'},
                                        'eemAppliedParam1': {'type': 'string'},
                                        'eemAppliedParam2': {'type': 'string'},
                                        'eemAppliedParam3': {'type': 'string'}
                                    }
                                    },
                    'eemInvestment': {'type': 'dict',
                                      'schema': {
                                          'investment': {'type': 'integer'},
                                          'investment': {'type': 'integer'}
                                      }
                                      },
                    'eemDate': {'type': 'dict',
                                'schema': {
                                    'applicationDate': {'type': 'datetime'},
                                    'contractDate': {'type': 'datetime'},
                                    'installationDate': {'type': 'datetime'}
                                }
                                },
                    'eemAssessment': {'type': 'dict',
                                      'schema': {
                                          'satisfactionAssessment': {'type': 'integer'},
                                          'complexityAssessment': {'type': 'integer'}
                                      }
                                      },
                },
            },
        },
        'modellingUnits': {
            'type': 'list',
            'schema': {
                'type': 'string'
            }
        },
        'hourlyData': {
            'type': 'boolean'
        },
        'buildingName': {
            'type': 'string'
        }
    }
}