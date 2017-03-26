
from walle.basic.main_py.singleton import Singleton

class VmList(metaclass=Singleton):
    def __init__(self):
        #TODO: 自己根据需求实现一个获取远程服务器列表
        pass

    def get_vm_param_you_like(self, param=None):
        return ['150.95.129.110']

