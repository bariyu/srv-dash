from constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

class BaseMetric(object):
    def __init__(self, name, calculate_period=1):
        """
            time_interval is in minutes
        """
        self.name = name
        self.calculate_period = calculate_period

    def get_continious_query_body(self):
        raise NotImplementedError

    def fill(self):
        """
            how should the continuous query fill empty values.
            influx does not fill when there are no data points in the interval anyway :/
        """
        return 'fill(0)'

    def group_by_extra_tags(self):
        """
            by default every continuous query should be tagged by app,
            metrics can override this to extend.
        """
        return []

    def get_continious_create_query(self, db_name):
        extra_group_tags = self.group_by_extra_tags()
        if extra_group_tags:
            extra_group_str = ", ".join(extra_group_tags)
            return \
                'CREATE CONTINUOUS QUERY {} ON "{}"\nBEGIN\n\t{} GROUP BY time({}m), app, {} {}\nEND'.format(self.name, db_name, self.get_continious_query_body(), self.calculate_period, extra_group_str, self.fill())
        return \
            'CREATE CONTINUOUS QUERY {} ON "{}"\nBEGIN\n\t{} GROUP BY time({}m), app {}\nEND'.format(self.name, db_name, self.get_continious_query_body(), self.calculate_period, self.fill())

    def get_basic_data_points_query(self, app=None):
        if not app:
            return 'SELECT * from {}'.format(self.name)
        return 'SELECT * from {} WHERE "app" = \'{}\''.format(self.name, app)

    def get_data_points_query(self, app=None):
        raise NotImplementedError

    def data_key(self):
        raise NotImplementedError

    def chart_type(self):
        raise NotImplementedError

    def unit_name(self):
        return ''

    def metric_title(self):
        return self.name

    def dict_to_key(self, d):
        return ','.join(['%s: %s' %(key, str(d[key])) for key in d.keys()])

    def get_series(self, influx_client, app=None):
        result_set = influx_client.query(self.get_data_points_query(app=app))
        items = result_set.items()
        series = []

        for item in items:
            if item[0][1]:
                series.append({
                    'name': self.dict_to_key(item[0][1]),
                    'data': [data for data in item[1]],
                })
            else:
                series.append({
                    'name': item[0][0],
                    'data': [data for data in item[1]]
                })

        return series
