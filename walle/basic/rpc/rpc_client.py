from walle.basic.rpc.rpc_error import RpcError
import sys
import os
import traceback
from walle.basic.serialization.serialize_by_pickle import PickleForSsh
import importlib


class RpcClient:
    serialize = PickleForSsh.dumps_to_str
    unserialize = PickleForSsh.loads_from_str

    @classmethod
    def do(cls, *args):
        if len(args) != 1:
            return RpcError.EXCEPT

        # 获取参数
        str_param = args[0]
        ssh_des = cls.unserialize(str_param)

        # 执行RPC
        # try:
        # method = RpcClient.rou

    @staticmethod
    def router_to_method(module_name, clazz_name, method_name):
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise AttributeError("import module:{0} failed, reason: {1}".format(module_name, e))

        if not hasattr(module, clazz_name):
            raise AttributeError("Module {0} doesn't have this class: {1}".format(module_name, clazz_name))
        clazz = getattr(module, clazz_name)

        if not hasattr(clazz, method_name):
            raise AttributeError("Class {0} doesn't have this method: {1}".format(clazz_name, method_name))
        return getattr(clazz, method_name)

    @staticmethod
    def reformat_traceback_info():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)[-1]
        tb_error = "TracebackRootCause: {filename}:{lineno}>>{function}()>>{text}\n{format_exc}".format(
            filename=os.path.basename(tb[0]),
            function=tb[2],
            lineno=tb[1],
            text=tb[3],
            format_exc="".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return tb_error
