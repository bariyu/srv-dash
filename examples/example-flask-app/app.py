from flask import Flask

from flask_srv_dash import SrvDashExtension

app = Flask(__name__)
exted = SrvDashExtension(app, 'example-flask-app', 'http://localhost:8000')

if __name__ == '__main__':
    app.run(port=8001, host='0.0.0.0', debug=True, threaded=True)
