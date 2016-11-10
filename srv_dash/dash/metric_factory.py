from base_metric import BaseMetric

class MetricFactory(object):
    def __init__(self):
        pass

    def get_metrics_classes(self):
        return BaseMetric.__subclasses__()
