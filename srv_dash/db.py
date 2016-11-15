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
        
        def dict_to_key(d):
            return ','.join(['%s: %s' %(key, str(d[key])) for key in d.keys()])

        metrics = {}
        for metric_instance in self.metric_instances:
            result_set = self.influx_client.query(metric_instance.get_data_points_query(app=app))
            items = result_set.items()
            series = []

            for item in items:
                if item[0][1]:
                    series.append({
                        'name': dict_to_key(item[0][1]),
                        'data': [data for data in item[1]],
                    })
                else:
                    series.append({
                        'name': item[0][0],
                        'data': [data for data in item[1]]
                    })

            metrics[metric_instance.name] = {
                'series': series,
                'data_key': metric_instance.data_key(),
                'chart_type': metric_instance.chart_type(),
                'name': metric_instance.name,
                'metric_title': metric_instance.metric_title(),
                'unit_name': metric_instance.unit_name()
            }
        return metrics

    def save_data(self, obj_list):
        json_body = [obj.serialize_to_influx_json() for obj in obj_list]
        self.influx_client.write_points(json_body)
        db_logger.debug('wrote new data points to influx')
