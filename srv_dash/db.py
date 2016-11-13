import json
import logging

db_logger = logging.getLogger()

from influxdb import InfluxDBClient
from dash.metric_factory import MetricFactory

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

    def get_metric_names(self):
        return [metric_instance.name for metric_instance in self.metric_instances]

    def get_all_metrics_data(self):
        metrics = {}
        for metric_instance in self.metric_instances:
            result_set = self.influx_client.query(metric_instance.get_data_points_query())
            #for data in result_set.get_points():
            # print data
            metrics[metric_instance.name] = result_set.get_points()
        return metrics

    def save_data(self, obj_list):
        json_body = [obj.serialize_to_influx_json() for obj in obj_list]
        self.influx_client.write_points(json_body)
        db_logger.debug('wrote new data point to influx')
