from __future__ import absolute_import
from builtins import map
from builtins import object
import datetime
import json
import requests
from . import models
from . import utils
from .exceptions import OnfleetException, OnfleetDuplicateKeyException


ONFLEET_API_ENDPOINT = "https://onfleet.com/api/v2/"

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        payload = None

        if isinstance(obj, models.Administrator):
            payload = {
                'name': obj.name,
                'email': obj.email
            }

            optional_properties = {
                'phone': 'phone',
            }
        elif isinstance(obj, models.Vehicle):
            payload = {'type': obj.vehicle_type}

            optional_properties = {
                'description': 'description',
                'license_plate': 'licensePlate',
                'color': 'color'
            }
        elif isinstance(obj, models.Worker):
            payload = {
            }

            optional_properties = {
                'vehicle': 'vehicle',
                'tasks': 'tasks',
                'name': 'name',
                'phone': 'phone',
                'teams': 'team_ids'
            }
        elif isinstance(obj, models.Address):
            payload = {
            }

            optional_properties = {
                'street': 'street',
                'number': 'number',
                'city': 'city',
                'country': 'country',
                'name': 'name',
                'apartment': 'apartment',
                'state': 'state',
                'postal_code': 'postalCode',
                'unparsed': 'unparsed',
            }
        elif isinstance(obj, models.Destination):
            payload = {
            }

            optional_properties = {
                'address': 'address',
                'location': 'location',
                'notes': 'notes',
            }
        elif isinstance(obj, models.Task):
            payload = {
                'merchant': obj.merchant,
                'executor': obj.executor,
                'destination': obj.destination,
                'recipients': obj.recipients,
            }

            optional_properties = {
                'notes': 'notes',
                'pickup_task': 'pickupTask',
                'dependencies': 'dependencies',
                'complete_after': 'completeAfter',
                'complete_before': 'completeBefore',
            }
        elif isinstance(obj, models.Recipient):
            payload = {
                'name': obj.name,
                'phone': obj.phone,
                'notes': obj.notes,
            }

            optional_properties = {}
        elif isinstance(obj, models.Administrator):
            payload = {
                'name': obj.name,
                'email': obj.email,
            }

            optional_properties = {'phone': obj.phone}

        if payload is None:
            return json.JSONEncoder.default(self, obj)
        else:
            for key, value in optional_properties.items():
                if hasattr(obj, key) and getattr(obj, key) is not None:
                    if isinstance(getattr(obj, key), datetime.datetime):
                        payload[value] = utils.to_unix_time(getattr(obj, key))
                    else:
                        payload[value] = getattr(obj, key)

            return payload


class Onfleet(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def __getattr__(self, k):
        return OnfleetCall(self.api_key, k)


class OnfleetCall(object):
    def __init__(self, api_key, path):
        self.api_key = api_key
        self.components = [path]

    def __getattr__(self, k):
        self.components.append(k)
        return self

    def __getitem__(self, k):
        self.components.append(k)
        return self

    def __call__(self, *args, **kwargs):
        url = "{}{}".format(ONFLEET_API_ENDPOINT, "/".join(self.components))
        if 'method' in kwargs:
            method = kwargs['method']
            del kwargs['method']
        else:
            method = "GET"

        parse_response = kwargs.get('parse_response', True)

        if 'parse_response' in kwargs:
            del kwargs['parse_response']

        fun = getattr(requests, method.lower())
        if len(args) > 0:
            data = ComplexEncoder().encode(args[0])
        else:
            data = None

        response = fun(url, data=data, params=kwargs, auth=(self.api_key, ''), verify=False)

        parse_dictionary = {
            'workers': models.Worker,
            'tasks': models.Task,
            'recipients': models.Recipient,
            'destinations': models.Destination,
            'organization': models.Organization,
            'admins': models.Administrator
        }

        parse_as = None
        for component, parser in parse_dictionary.items():
            if component in self.components:
                parse_as = parser

        if method.lower() != 'delete':
            json_response = response.json()

            if 'code' in json_response:
                message = json_response['message']
                cause = message.get('cause', '')

                if isinstance(cause, dict) and cause['type'] == 'duplicateKey':
                    raise OnfleetDuplicateKeyException("{}: {} (value: '{}', key: '{}')" \
                        .format(message['error'], message['message'], cause['value'], cause['key']))
                raise OnfleetException("{}: {} ({})" \
                    .format(message['error'], message['message'], cause))

            if parse_response and parse_as is not None:
                if isinstance(json_response, list):
                    return list(map(parse_as.parse, json_response))
                else:
                    return parse_as.parse(json_response)
            else:
                return json_response
        return None
