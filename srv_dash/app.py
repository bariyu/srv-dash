import sys
import ConfigParser
import logging
import json
from functools import wraps


from flask import Flask, abort, request, Response
from models import HttpServerReqResp
from db import InfluxDBCli

logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s')
log = logging.getLogger()

app = Flask(__name__)
conf_parser = ConfigParser.ConfigParser()
conf_parser.read("../config/srv-dash.ini")

db_cli = InfluxDBCli(
    conf_parser.get('influxdb', 'uri'),
    conf_parser.getint('influxdb', 'port'),
    conf_parser.get('influxdb', 'username'),
    conf_parser.get('influxdb', 'password'),
    conf_parser.get('influxdb', 'database')
)

def check_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_enabled = conf_parser.get('auth', 'enabled')
        auth_key = None
        if auth_enabled:
            auth_key = conf_parser.get('auth', 'auth-key')
        if auth_enabled and request.headers.get('X-Auth-Key') != auth_key:
            return abort(401)
        return func(*args, **kwargs)
    return decorated


def process_data(data_list):
    obj_list = [HttpServerReqResp(**data) for data in data_list]
    db_cli.save_data(obj_list)


@app.route("/add_data", methods=['POST'])
@check_auth
def add_data():
    request_data = json.loads(request.data)
    if type(request_data) != list:
        abort(400)
    try:
        process_data(request_data)
        return Response(response=json.dumps({}),
                    status=200,
                    mimetype="application/json")
    except ValueError as e:
        return Response(response=json.dumps({'error': '%s' %(e)}),
                    status=400,
                    mimetype="application/json")


if __name__ == '__main__':
    try:
        app.run(port=conf_parser.getint('server', 'port'), host='0.0.0.0', debug=conf_parser.get('server', 'debug'), threaded=True)
    except Exception as e:
        log.critical('failed initing srv-dash exiting')
        log.critical('%s' %(e))
        sys.exit(1)
