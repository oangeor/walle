import os
import logging

from walle.basic.env_manager import env_mng
from walle.basic.serialization.serialize_by_pickle import PickleForSsh


class RemoteEnv:
    def __init__(self, test_param="", ):
        # TODO: 通过参数控制远程执行环境
        self.test_param = test_param

    def __str__(self):
        return "RemoteEnv:" + str(self.__dict__)


class SshRpcDestination:
    walle_py = 'walle/basic/main_py/main.py -m agent'
    root_entry = 'walle/basic'

    def __init__(self, app_name="", vm_name="", service_name="", method_name="", module_name="",
                 method_args=None,
                 method_kwargs=None,
                 env=None
                 ):
        self.method_args = method_args or dict()
        self.method_kwargs = method_kwargs or list()
        self.module_name = module_name
        self.app_name = app_name
        self.vm_name = vm_name
        self.service_name = service_name
        self.method_name = method_name

        # self.main_py_pwd = rpc_lite_entry.__file__
        now_pwd = os.path.realpath(__file__)
        py_code_pwd = now_pwd.split(self.root_entry)[0]
        self.main_py_pwd = py_code_pwd + self.walle_py
        self.env = env or RemoteEnv()

    @classmethod
    def init_by_call(cls, call, call_args=None, call_kwargs=None, vm_name='', env=None):
        service, method = call.__qualname__.split(".")
        return cls(
            module_name=call.__module__,
            service_name=service,
            method_name=method,
            method_args=call_args,
            method_kwargs=call_kwargs,
            vm_name=vm_name,
            env=env
        )

    def gen_rpc_info(self):
        return self.service_name + '.' + self.method_name

    def gen_shell_cmd(self):
        if not all((self.module_name, self.service_name, self.method_name)):
            raise ValueError("Missing Key Parameter")

        nice = "nice -n 10 " if env_mng.renice else ""
        python3 = nice + env_mng.python3_path

        py_path = self.main_py_pwd
        py_param = PickleForSsh.dumps_to_str(self)

        logging.info("{python3} {py_path}  {py_param}".format(
            python3=python3, py_path=py_path, py_param=py_param))
        return "{python3} {py_path}  {py_param}".format(
            python3=python3, py_path=py_path, py_param=py_param)
