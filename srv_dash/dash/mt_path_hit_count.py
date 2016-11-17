from base_metric import BaseMetric
from constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

class PathHitCountMetric(BaseMetric):
    def __init__(self):
        BaseMetric.__init__(self, 'path_hit_count')

    def get_continious_query_body(self):
        return 'SELECT count("ip") INTO "{}" FROM {}'.format(self.name, HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME)

    def group_by_extra_tags(self):
        return ["path"]

    def get_data_points_query(self, app=None):
        if not app:
            return 'SELECT * from {} GROUP BY "path"'.format(self.name)
        return 'SELECT * from {} WHERE "app" = \'{}\' GROUP BY "path"'.format(self.name, app)

    def get_data_points_query_for_a_path(self, path, app=None):
        if not app:
            return 'SELECT * from {} WHERE "path" = \'{}\''.format(self.name, path)
        return 'SELECT * from {} WHERE "app" = \'{}\' AND "path" = \'{}\''.format(self.name, app, path)

    def data_key(self):
        return 'count'

    def chart_type(self):
        return 'linear'

    def metric_title(self):
        return '# of requests for a path (most used {} paths)'.format(self.max_different_path())

    def sum_query(self, app=None):
        if not app:
            return 'SELECT SUM("count") from {} GROUP BY "path"'.format(self.name)
        return 'SELECT SUM("count") from {} WHERE "app" = \'{}\' GROUP BY "path"'.format(self.name, app)

    def max_different_path(self):
        return 5

    def get_series(self, influx_client, app=None):
        max_result_set = influx_client.query(self.sum_query(app=app))
        items = max_result_set.items()
        path_sums = []
        for item in items:
            path_sum_parsed = [data for data in item[1]][0]['sum']
            path_sums.append({
                'sum': path_sum_parsed,
                'path': item[0][1]['path'],
            })
        path_sums = sorted(path_sums, key=lambda x: x['sum'], reverse=True)
        max_different_path = self.max_different_path()
        if max_different_path < len(path_sums):
            path_sums = path_sums[:max_different_path]

        series = []
        for path in path_sums:
            result_set = influx_client.query(self.get_data_points_query_for_a_path(path['path'], app=app))
            items = result_set.items()
            item = items[0]
            series.append({
                'name': 'path: {}'.format(path['path']),
                'data': [data for data in item[1]]
            })
        return series
