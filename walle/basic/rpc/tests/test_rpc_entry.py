import unittest
import sys
from walle.basic.rpc.rpc_entry import rpc
from walle.app.example.demo import ExampleService


class TestRpcEntry(unittest.TestCase):

    @unittest.skipUnless(sys.platform in ["darwin"], "Only test in local")
    def test_func(self):
        call = ExampleService.example_func
        call_kwargs = dict(msg="ping")
        vms = ["127.0.0.1"]
        return_obj = rpc.call_vms_by_list(
            call=call,
            call_kwargs=call_kwargs,
            vms=vms,
        )
        print(return_obj)
        self.assertTrue(return_obj)


if __name__ == '__main__':
    unittest.main()
