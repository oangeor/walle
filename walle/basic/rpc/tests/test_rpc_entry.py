import unittest
import sys
from walle.basic.rpc.rpc_entry import rpc
from walle.common.example.demo import ExampleService
from walle.basic.rpc.ssh_rpc_destination import SshRpcDestination, RemoteEnv
from walle.basic.serialization.serialize_by_pickle import PickleForSsh


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

    def test_gen_shell_cmd(self):
        test_param = "test"
        string = SshRpcDestination.init_by_call(
            SshRpcDestination.init_by_call,
            env=RemoteEnv(test_param=test_param)
        ).gen_shell_cmd()
        obj = PickleForSsh.loads_from_str(string.split()[-1])
        env = obj.env
        self.assertEqual(env.test_param, test_param)


if __name__ == '__main__':
    unittest.main()
