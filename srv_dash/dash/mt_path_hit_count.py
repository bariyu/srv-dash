from base_metric import BaseMetric
from constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

class PathHitCountMetric(BaseMetric):
    def __init__(self):
        BaseMetric.__init__(self, 'path_hit_count')

    def get_continious_query_body(self):
        return 'SELECT count("ip") INTO "{}" FROM {}'.format(self.name, HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME)

    def group_by_extra_tags(self):
        return ["path"]
