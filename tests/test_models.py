import unittest

from srv_dash.models import HttpServerReqResp

class TestModels(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model_init(self):
        with self.assertRaises(ValueError) as context:
            srr = HttpServerReqResp()
            pass

        self.assertTrue('cannot create ServerReqResp obj missing required field' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
