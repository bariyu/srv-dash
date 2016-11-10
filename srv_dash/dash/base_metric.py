from constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

class BaseMetric(object):
    def __init__(self, name, calculate_period=5):
        """
            time_interval is in minutes
        """
        self.name = name
        self.calculate_period = calculate_period

    def get_continious_query_body(self):
        raise NotImplementedError

    def get_continious_create_query(self, db_name):
        return \
            'CREATE CONTINUOUS QUERY {} ON "{}"\nBEGIN\n\t{} GROUP BY time({}m)\nEND'.format(self.name, db_name, self.get_continious_query_body(), self.calculate_period)
