import logging

models_logger = logging.getLogger('models')

required_fields = [
    # app specific
    'app', # e.g. srv-dash

    # request specific
    'time', # e.g. 2016-11-10T23:00:00Z
    'method', # e.g. POST
    'path', # e.g. /add_data
    'full_path', # e.g. /add_data?x=1,
    'is_xhr', # e.g. False
    'user-agent', # e.g. Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
    'content-length', # e.g. 348
    'referer', # e.g. https://www.google.com

    # response specific
    'status', # e.g. 200
    'resp_time', # e.g. 123 (timespent in server in ms)
]

optional_fields = [
    # app specific
    'server_name' # e.g. node01

    # request specific

    # response specific
]

all_fields = required_fields + optional_fields

class HttpServerReqResp(object):
    def __init__(self, **kwargs):
        _data = {}

        for key in kwargs:
            _data[key] = kwargs[key]

        for key in required_fields:
            if not _data.get(key):
                err_desc = 'cannot create ServerReqResp obj missing required field: %s' %(key)
                models_logger.error(err_desc)
                raise ValueError(err_desc)

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, value):
        if key in all_fields:
            self._data[key] = value
