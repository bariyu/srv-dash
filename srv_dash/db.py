import json
import logging

db_logger = logging.getLogger()

from influxdb import InfluxDBClient

class InfluxDBCli(object):
    def __init__(self, host, port, username, password, db_name):
        db_logger.info('inited influx db cli')
        self.influx_client = InfluxDBClient(host, port, username, password, db_name)
        self.influx_client.create_database(db_name)

    def save_data(self, obj_list):
        json_body = [obj.serialize_to_influx_json() for obj in obj_list]
        self.influx_client.write_points(json_body)
        db_logger.info('wrote new data point to influx')
