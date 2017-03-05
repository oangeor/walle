from enum import Enum
from walle.basic.failure.problem_type import ProblemType


class ErrorCode(Enum):
    E_CLIENT_NO_PYTHON = '客户端没有安装python3'
    E_CLIENT_NO_DEPLOY_CODE = '客户端没有部署最新的代码'
    E_CLIENT_CODE_EXCEPTION = '客户端代码抛出错误'
    E_RPC_SSH_CONNECT = 'RPC SSH建立连接失败'
    E_RPC_SSH_SEND = 'RPC SSH发送数据失败'
    E_RPC_SSH_READ = 'RPC SSH读取数据失败'
    E_RPC_REMOTE_FAILED = 'RPC 远程运行错误'
    E_RPC_NO_CONTENT = 'RPC返回内容为空'
    E_PICKLE_DECODE = 'PICKLE解码失败'
    E_PICKLE_ENCODE = 'PICKLE编码失败'
    E_PICKLE_SUCCESS = 'PICKLE解码成功，但是上下文错误'
    E_ENDLESS_LOOP = '死循环'
    Y_HAS_CONTENT = '业务成功'
    Y_NO_CONTENT = '系统成功'
    E_RPC_JSON_LOADS = 'RPC JSON解码失败'
    E_HTTP_TIMEOUT = 'HTTP TIMEOUT'
    E_HTTP_ERROR = 'HTTP ERROR'

    def __str__(self):
        return self.name


class TechFailKeyError():
    def __init__(self, error_code, target_vm='', target_app=''):
        super().__init__()
        self.error_code = error_code.name
        if self.error_code.startswith('E_'):
            self.problem_type = ProblemType.rpc_error
        else:
            self.problem_type = ProblemType.success

        self.target_vm = target_vm
        self.target_app = target_app
        # self.problem_detail = ";".join((error_code.value, Trace.get_trace()))

    # def _to_protobuf_ext(self, node):
    #     node.error_code = self.error_code
    #     node.error_msg = ErrorCode[self.error_code].value
    #     node.target_vm = self.target_vm
    #     self.add_aggr_info(AggrKey.target_vm, self.target_vm)

    def __str__(self):
        # 容错，python的泛型特性，业务侧传入的error_code 可能直接就是str了
        error_code_name = self.error_code if isinstance(self.error_code, str) else self.error_code.name
        return "错误码：{error_code_name}, 目标机器: {target_vm}".format(
            error_code_name=error_code_name,
            target_vm=self.target_vm
        )

    def __repr__(self):
        return self.__str__()
