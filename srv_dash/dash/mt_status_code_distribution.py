from base_metric import BaseMetric
from constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

class StatusCodeDistributionMetric(BaseMetric):
    def __init__(self):
        BaseMetric.__init__(self, 'status_code_distribution')

    def get_continious_query_body(self):
        return 'SELECT COUNT("ip") INTO "{}" FROM {}'.format(self.name, HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME)

    def data_key(self):
        return 'count'

    def chart_type(self):
        return 'linear'

    def unit_name(self):
        return ''

    def group_by_extra_tags(self):
        return ['"status-code"']

    def metric_title(self):
        return 'distribution of status codes that server produces'

    def get_data_points_query(self, app=None):
        if not app:
            return 'SELECT * from {} GROUP BY "status-code" = \'{}\''.format(self.name)
        return 'SELECT * from {} WHERE "app" = \'{}\' GROUP BY "status-code"'.format(self.name, app)
