companies= {
    'resource_methods': ['GET'],
    'item_methods': ['PATCH'],
    'item_lookup_field': 'companyId',
    'doc': {
            'body':
            """
            <p>Companies resource to edit company information.</p> 
            """,
            'title':'Companies',
            },              
    'schema' : {
        'companyId': {
                      'type': 'integer',
                      'required': True,
                      },
        'domain': {
                   'type': 'string',
                   'required': True,
                   'minlength' : 3,
                   'maxlength' : 12,
        },
        'name':{
                'type':'string',
                'required':True
        },
        'firstNameContactCompany': {
            'type' : 'string',
            'minlength' : 1,
            'maxlength' : 50,
            'required' : True,
        },
        'firstSurnameContactCompany': {
            'type' : 'string',
            'minlength' : 1,
            'maxlength' : 50,
            'required' : True,
        },
        'secondSurnameContactCompany': {
            'type' : 'string',
            'minlength' : 1,
            'maxlength' : 50,
        },
        'emailContactCompany': {
            'type' : 'string',
            'minlength' : 7,
            'maxlength' : 50,
            'required' : True,
        },
        'street' : {
            'type' : 'string',
        },
        'postalCode' : {
            'type' : 'string',
        },
        'city' : {
            'type' : 'string',
        },
        'cityCode' : {
            'type' : 'string',
        },
        'province' : {
            'type' : 'string',
        },
        'provinceCode' : {
            'type' : 'string',
        },
        'country' : {
            'type' : 'string',
        },
        'countryCode' : {
            'type' : 'string',
            'minlength': 2,
            'maxlength': 2,
        },
        'parcelNumber' : {
            'type': 'string',
        },
    }
}

