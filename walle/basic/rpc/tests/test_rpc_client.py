
import unittest
from walle.basic.rpc.rpc_client import RpcClient


class TestRpcClient(unittest.TestCase):
    def test_reformat_traceback_info(self):
        try:
            raise Exception("HelloWorld")
        except BaseException:
            tb_error = RpcClient.reformat_traceback_info()
            print(tb_error)
            self.assertIn("TracebackRootCause", tb_error)
            self.assertIn("test_rpc_client.py", tb_error)
            self.assertIn('''Exception("HelloWorld")''', tb_error)
