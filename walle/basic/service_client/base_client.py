from walle.basic.rpc.ssh_rpc_destination import RemoteEnv
from walle.basic.rpc.rpc_entry import rpc
from walle.common.example.demo import ExampleService
from walle.basic.rpc.vm_list import VmList


class BaseClient:
    @classmethod
    def call_vm(cls):
        call = ExampleService.example_func
        call_kwargs = dict(msg="ping")

        vms = VmList().get_vm_param_you_like()  # 自己根据需求更改

        return_obj = rpc.call_vms_by_list(
            call=call,
            call_kwargs=call_kwargs,
            vms=vms,
        )

        print(return_obj)
        return return_obj
