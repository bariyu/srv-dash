# srv-dash
srv-dash is a dashboard that helps you monitor your servers stats/performance. It does this by exposing a REST API. What you have to do is providing your server logs constantly to srv-dash via the REST API.

### Requirements
- influxdb >= 1.0
- Python => 2.7 (I have never tested with python 3+)

### Getting Started
Clone this repo to where you want to run your dashboard. Configure your dashboard with `srv-dash.ini` file which resides under the `config` folder.

First install requirement with with `pip install -r requirements.txt` then run with `python app.py` in the `srv_dash` folder. Your dashboard will be avaliable on `http://localhost:8000` by default.

srv-dash will automatically show a dashboard for its own server. You can start monitoring your apps by using the REST API.

### Using the API

You can test using the api by the following curl command `curl -X POST -H 'Content-Type: application/json' --data-binary @example_data.json http://localhost:8000/add_data` in the `tests` folder. But remember to set the `req-Date` to current time so that you will start seeing metrics for immediately.

Note: If you have enabled authentication from the `srv-dash.ini` config file. You should send your `auth-key` defined in the config file, in the `X-Auth-Key` header field.

Here are some screenshots of how your dashboard is going to look like.
![ss1](https://raw.githubusercontent.com/bariyu/srv-dash/master/screenshots/1.png)

![ss2](https://raw.githubusercontent.com/bariyu/srv-dash/master/screenshots/2.png)

### Clients
My aim is to create extensions to mostly used frameworks around to make applications integrate into srv-dash with a one liner.
-  [Flask extension](https://github.com/bariyu/srv-dash-flask-ext) & [example one liner app](https://github.com/bariyu/srv-dash/blob/master/examples/example-flask-app/app.py)
- More to come soon and I would be very happy if you want to provide one for your framework.


### Metrics
Metrics are calculated by using [influxdb continious queries](https://docs.influxdata.com/influxdb/v1.1/query_language/continuous_queries/) every 1 minute.
I have included 5 basic metrics to be calculated and srv-dash draws each of one them.

- [avg_server_time](https://github.com/bariyu/srv-dash/blob/master/srv_dash/dash/mt_avg_server_time.py): calculates mean server response time for your app
- [perc_98_server_time](https://github.com/bariyu/srv-dash/blob/master/srv_dash/dash/mt_98_perc_server_time.py) 98th percentile of server response time for your app
- [path_hit_count](https://github.com/bariyu/srv-dash/blob/master/srv_dash/dash/mt_path_hit_count.py) shows the most used 5 paths of your app.
- [slowest_server_time_path](https://github.com/bariyu/srv-dash/blob/master/srv_dash/dash/mt_slowest_paths.py) shows the slowest 5 paths according to server time for your app.
- [status_code_distribution](https://github.com/bariyu/srv-dash/blob/master/srv_dash/dash/mt_status_code_distribution.py) shows the http status code distribution your server produces over.

#### Adding your custom metrics
To add your custom metrics or a generic metric that you think that can be useful. Create `mt_<your_metric_name>.py` file under the folder `srv_dash/dash/` and then register that metric to `__init__.py` by importing, in the same folder. What you need to for defining your metric implementing a new class by subclassing [`BaseMetric`](https://github.com/bariyu/srv-dash/blob/master/srv_dash/dash/base_metric.py).

Every metric class that extends `BaseMetric` is automatically registered when you launch the dashboard by creating a continious query for it.

I really appreciate if you add new metrics then open a submit it with a pull-request so that everybody can benefit from them.

To modify the react dashboard app, you should go to `srv_dash/react` folder and modify it. It is bundled by [webpack](https://www.influxdata.com/). Use `npm run-script webpack-dev` to create the bundle file.


### Tech Stack
This part is optional you can skip if you do not care about it. I just wanted to summarize the tech stack behind this app.

- Server
    - [Python](https://www.python.org/)
    - [Flask](http://flask.pocoo.org/)
    - [Influxdb](https://www.influxdata.com/)


- Client
    - [React](https://facebook.github.io/react/)
    - [react-router](https://github.com/ReactTraining/react-router)
    - [redux](https://github.com/reactjs/redux)
    - [blueprint.js](http://blueprintjs.com/)
    - [plottable.js](http://plottablejs.org/)
