from walle.basic.rpc.rpc_client import RpcClient
from walle.basic.env_manager import env_mng


class LocalRpc:
    def call_vms_by_des(self, des, hosts, rpc_info):
        func = RpcClient.router_to_method(des.module_name, des.service_name, des.method_name)
        return {env_mng.hostname: func(**des.method_kwargs)}
