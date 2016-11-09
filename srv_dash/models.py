import logging
import json

models_logger = logging.getLogger()

required_fields = [
    # app specific
    'app', # e.g. srv-dash

    # request specific
    'scheme', # e.g. https
    'method', # e.g. POST
    'path', # e.g. /add_data
    'ip', # e.g. 127.0.0.1

    # from http headers
    'req-Date', # e.g. 2016-11-10T23:00:00Z
    'req-Content-Length', # e.g. 348
    'req-Content-Type', # e.g. application/x-www-form-urlencoded
    'Origin', # e.g. http://www.example-social-network.com
    'User-Agent', # e.g. Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko

    # response specific
    'status-code', # e.g. 200
    'resp-time', # e.g. 123 (timespent in server in ms)

    # from http headers
    'resp-Date', # e.g. 2016-11-10T23:00:00Z
    'resp-Content-Length', # e.g. 348
    'resp-Content-Type', # e.g. application/x-www-form-urlencoded
]

optional_fields = [
    # app specific
    'server_name' # e.g. node01

    # request specific
    'full_path', # e.g. /add_data?x=1, # query params may include sensitive data like user_ids etc. making it optional

    # from http headers
    'Referer', # e.g. https://www.google.com

    # response specific
]

all_fields = required_fields + optional_fields

class HttpServerReqResp(object):
    def __init__(self, **kwargs):
        self._data = {}

        for key in kwargs:
            if key in all_fields:
                self._data[key] = kwargs[key]

        for key in required_fields:
            if self._data.get(key) is None:
                err_desc = 'missing required field: %s' %(key)
                models_logger.error(err_desc)
                raise ValueError(err_desc)

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        if key in all_fields:
            self._data[key] = value

    def to_json(self):
        return self._data

    def __repr__(self):
        return json.dumps(self._data, indent=2)

    def serialize_to_influx_json(self):
        tags = [
            'app',
            'scheme',
            'method',
            'path',
            'User-Agent',
            'status-code',
            'server_name',
            'Referer'
        ]
        fields = [
            'ip',
            'req-Content-Length',
            'req-Content-Type',
            'Origin',
            'resp-time',
            'resp-Date',
            'resp-Content-Length',
            'resp-Content-Type',
            'full_path'
        ]
        tags_dict = {}
        fields_dict = {}
        for key in self._data.keys():
            if key in tags:
                tags_dict[key] = self._data[key]
            elif key in fields:
                fields_dict[key] = self._data[key]
        return {
            'measurement': 'server_req_resp',
            'tags': tags_dict,
            'fields': fields_dict,
            'time': self._data['req-Date']
        }
