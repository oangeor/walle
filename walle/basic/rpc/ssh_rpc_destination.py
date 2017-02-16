class SshRpcDestination:

    walle_py = 'main_py/src/-m agent'

    def __init__(self, app_name="", vm_name="", service_name="", method_name="", module_name="",
                 method_args=None,
                 method_kwargs=None,
                 env=None
                 ):
        method_args = method_args or tuple()
        method_kwargs = method_kwargs or dict()



    @classmethod
    def init_by_call(cls, call, call_args=None, call_kwargs=None, vm_name='', env=None):
        service, method = call.__qualname__.split(".")
        return cls()
