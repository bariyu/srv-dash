import sys
import ConfigParser
import logging

from flask import Flask
from models import ServerReqResp

logging.basicConfig(format='%(asctime)s [%(threadName)16s][%(module)14s][%(levelname)8s] %(message)s')
log = logging.getLogger()

def init_and_run_app():
    try:
        conf_parser = ConfigParser.ConfigParser()
        conf_parser.read("../config/srv-dash.ini")

        app = Flask(__name__)
        app.run(port=conf_parser.getint('server', 'port'), host='0.0.0.0', debug=conf_parser.get('server', 'debug'), threaded=True)
    except Exception as e:
        log.critical('failed initing srv-dash exiting')
        log.critical('%s' %(e))
        sys.exit(1)


if __name__ == '__main__':
    init_and_run_app()
