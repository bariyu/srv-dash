from base_metric import BaseMetric
from constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

class AverageServerTimeMetric(BaseMetric):
    def __init__(self):
        BaseMetric.__init__(self, 'avg_server_time')

    def get_continious_query_body(self):
        return 'SELECT mean("resp-time") INTO "{}" FROM {}'.format(self.name, HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME)
