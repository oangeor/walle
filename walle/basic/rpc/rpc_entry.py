import os
import logging
from walle.basic.env_manager import env_mng
from walle.basic.rpc.ssh_rpc_destination import RemoteEnv, SshRpcDestination
import traceback
# TODO# if env_mng.is_in_local():
from walle.basic.rpc.local_rpc import LocalRpc as SshRpc


class RpcEntry:
    def __init__(self):
        self.ssh_client = SshRpc()

    def _do_rpc(self, des, hosts, rpc_info):
        # return self.ssh_client.call_vms_by_des(des, [env])
        return self.ssh_client.call_vms_by_des(des, hosts, rpc_info)

    def call_vm_by_interface(self, call_method, call_kwargs=None, vm_name='', env=None):
        call_kwargs = call_kwargs or dict()
        env = env or RemoteEnv()

        assert isinstance(call_kwargs, dict)
        assert callable(call_method)
        return self.call_vm

    def call_vm(self, call, params=None, vm_name='', env=None):
        params = params or dict()
        assert callable(call)
        assert isinstance(params, dict)

        try:
            des = SshRpcDestination.init_by_call(call=call, call_kwargs=params, vm_name=vm_name, env=env)
            result = self._do_rpc(des=des, hosts=[vm_name], rpc_info=des.gen_rpc_info())
            return result.popitem()[1]
        except BaseException:
            logging.error(traceback.format_exc())
            return []

    def call_vms_by_list(self, call, call_kwargs, vms, env=None):
        assert callable(call)
        assert isinstance(call_kwargs, dict)

        des = SshRpcDestination.init_by_call(call=call, call_kwargs=call_kwargs, env=env)
        return self._do_rpc(des=des, hosts=vms, rpc_info=des.gen_rpc_info())

rpc = RpcEntry()
