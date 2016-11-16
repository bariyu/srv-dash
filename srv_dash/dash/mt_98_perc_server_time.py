from base_metric import BaseMetric
from constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

class Perc98ServerTimeMetric(BaseMetric):
    def __init__(self):
        BaseMetric.__init__(self, 'perc_98_server_time')

    def get_continious_query_body(self):
        return 'SELECT percentile("resp-time", 98) INTO "{}" FROM {}'.format(self.name, HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME)

    def data_key(self):
        return 'percentile'

    def chart_type(self):
        return 'linear'

    def unit_name(self):
        return 'ms'

    def metric_title(self):
        return '98th percentile server response time'
