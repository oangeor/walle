class RemoteEnv:
    def __init__(self, grep_time='', shadow=False, min_rt_threshold=10, job_id=0):
        self.grep_time = grep_time
        self.shadow = shadow
        self.min_rt_threshold = min_rt_threshold
        self.job_id = job_id

    def __str__(self):
        return "RemoteEnv:" + str(self.__dict__)


class SshRpcDestination:
    walle_py = 'main_py/src/-m agent'

    def __init__(self, app_name="", vm_name="", service_name="", method_name="", module_name="",
                 method_args=None,
                 method_kwargs=None,
                 env=None
                 ):
        self.method_args = method_args or dict()
        self.method_kwargs = method_kwargs or list()
        self.module_name = module_name
        self.app_name =app_name
        self.vm_name = vm_name
        self.service_name = service_name
        self.method_name = method_name

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
