import sys
import ConfigParser
import logging
import json
from functools import wraps
from datetime import datetime
from time import time

from flask import Flask, abort, request, Response, g, render_template
from tzlocal import get_localzone

from models import HttpServerReqResp
from db import InfluxDBCli

app = Flask(__name__)
conf_parser = ConfigParser.ConfigParser()
conf_parser.read("../config/srv-dash.ini")

if conf_parser.get('server', 'debug'):
    logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s', stream=sys.stdout, level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s', stream=sys.stdout, level=logging.INFO)
log = logging.getLogger()

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


@app.route("/", methods=['GET'])
def index():
    db_cli.get_all_metrics_data()
    return render_template('index.html')


@app.before_request
def log_request():
    g.req_start_time = time()
    g.req_resp_meta_data = {
        'app': 'srv-dash',
        'scheme': 'http' if request.url.startswith('http://') else 'https',
        'method': request.method,
        'path': request.path,
        'ip': request.remote_addr,
        'req-Date': datetime.now(get_localzone()).isoformat(),
        'req-Content-Length': int(request.headers.get('Content-Length', 0)) if type(request.headers.get('Content-Length')) == str else 0,
        'req-Content-Type': request.headers.get('Content-Type'),
        'Origin': request.headers.get('Origin', ''),
        'User-Agent': request.headers.get('User-Agent'),
    }


@app.after_request
def log_response(response):
    response_meta_data = {
        'status-code': response.status_code,
        'resp-time': int((time() - g.req_start_time) * 1000),
        'resp-Date': datetime.now(get_localzone()).isoformat(),
        'resp-Content-Length': int(response.headers.get('Content-Length', 0)),
        'resp-Content-Type': response.headers.get('Content-Type'),
    }
    g.req_resp_meta_data.update(response_meta_data)
    process_data([g.req_resp_meta_data])
    return response


if __name__ == '__main__':
    try:
        app.run(port=conf_parser.getint('server', 'port'), host='0.0.0.0', debug=conf_parser.get('server', 'debug'), threaded=True)
    except Exception as e:
        log.critical('failed initing srv-dash exiting')
        log.critical('%s' %(e))
        sys.exit(1)
