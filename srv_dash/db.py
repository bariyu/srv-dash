import json
import logging

from influxdb import InfluxDBClient

from dash.metric_factory import MetricFactory
from dash.constants import HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME

db_logger = logging.getLogger()

class InfluxDBCli(object):
    def __init__(self, host, port, username, password, db_name):
        db_logger.info('inited influx db cli')
        self.db_name = db_name
        self.influx_client = InfluxDBClient(host, port, username, password, db_name)
        self.influx_client.create_database(db_name)
        self.metric_instances = [klass() for klass in MetricFactory().get_metrics_classes()]

        self.init_metrics()

    def init_metrics(self):
        for metric_instance in self.metric_instances:
            self.influx_client.query(metric_instance.get_continious_create_query(self.db_name))
            db_logger.debug('inited metric {}'.format(metric_instance.name))

    def get_app_names(self):
        result_set = self.influx_client.query('SHOW TAG VALUES WITH KEY = "app"')
        tag_values = result_set.get_points(HTTP_SERVER_REQ_RESP_MEASUREMENT_NAME)
        return [tag.get('value') for tag in tag_values]

    def get_metric_names(self):
        return [metric_instance.name for metric_instance in self.metric_instances]

    def get_metrics(self, app=None):
        metrics = {}
        for metric_instance in self.metric_instances:
            result_set = self.influx_client.query(metric_instance.get_data_points_query(app=app))
            data_points = result_set.get_points(metric_instance.name)
            metrics[metric_instance.name] = {
                'data': [data_point for data_point in data_points],
            }
        return metrics

    def save_data(self, obj_list):
        json_body = [obj.serialize_to_influx_json() for obj in obj_list]
        self.influx_client.write_points(json_body)
        db_logger.debug('wrote new data point to influx')
