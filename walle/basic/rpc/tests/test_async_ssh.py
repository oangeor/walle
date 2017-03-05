import os
import pwd
import sys
import unittest

from walle.basic.rpc.my_async_ssh import MyAsyncSsh


@unittest.skipUnless(sys.platform in ["darwin"], "Only test in local")
class TestAsyncSsh(unittest.TestCase):
    def test_run_cmd(self):
        # client = MyAsyncSsh(username=pwd.getpwuid(os.getuid())[0])
        username = "root"
        client = MyAsyncSsh(username=username)
        hosts = ['150.95.129.110', '150.95.129.110']

        ret = client.run_command_on_hosts(hosts, "echo 123")
        for h in hosts:
            print(ret[h])
            self.assertEqual(ret[h].stdout.strip(), "123")


if __name__ == "__main__":
    unittest.main()
