import time
import logging
from io import StringIO
import asyncssh

from walle.basic.rpc.my_async_ssh import MyAsyncSsh
from walle.basic.env_manager import env_mng
from walle.basic.failure.tech_fail_key_error import ErrorCode, TechFailKeyError
from walle.basic.serialization.serialize_by_pickle import PickleForSsh


class AsshRpc:
    def __init__(self):
        self.client = MyAsyncSsh(key_files=('~/.ssh/id_rsa',))

    def call_vms_by_des(self, des, hosts, rpc_info):
        return self.call_vms(hosts, rpc_info, des=des)

    def call_vms(self, hosts, rpc_info, cmd=None, des=None):
        try:
            cmd = cmd or des.gen_shell_cmd()
        except AttributeError:
            pass

        if not cmd or not hosts or not isinstance(hosts, list):
            raise ValueError("Ssh args cannot be empty.")

        start_time = time.time()
        results = self.client.run_command_on_hosts(
            hosts, cmd,
            timeout=env_mng.rpc_timeout,
            shell="bash -cl",
            use_shell=True,
        )

        logging.debug(results)
        if not results:
            logging.warning("No ssh results returned!")
            return {host: '' for host in hosts}

        return_map = {}
        for host, result in results.items():
            result_state, rpc_result = self.read_result_by_host(cmd, host, result)
            if rpc_result:
                return_map[host] = rpc_result
            elif result_state.error_code in [ErrorCode.E_RPC_SSH_CONNECT.name, ErrorCode.E_RPC_NO_CONTENT.name]:
                return_map[host] = result_state
        return return_map

    @staticmethod
    def read_result_by_host(cmd, host, result):
        if not isinstance(result, asyncssh.SSHCompletedProcess):
            tech_fail_key_error = TechFailKeyError(error_code=ErrorCode.E_RPC_SSH_CONNECT, target_vm=host)
            return tech_fail_key_error, None

        # read the stdout
        try:
            return_line_list = [line.strip() for line in StringIO(result.stdout)]
        except Exception as e:
            # print("Host[" + str(host) + "] read_line EXCEPT: {}".format(str(e)))
            tech_fail_key_error = TechFailKeyError(error_code=ErrorCode.E_RPC_SSH_READ, target_vm=host)
            return tech_fail_key_error, None

        # result contains nothing
        if len(return_line_list) == 0:
            tech_fail_key_error = TechFailKeyError(error_code=ErrorCode.E_RPC_NO_CONTENT, target_vm=host)
            return tech_fail_key_error, None

        # result contains at lease one line:
        result_single_line = return_line_list[-1]

        # Unpickling
        pickle_result = PickleForSsh.loads_from_str(result_single_line)
        if pickle_result:
            return TechFailKeyError(error_code=ErrorCode.Y_HAS_CONTENT, target_vm=host), pickle_result
            # return "Y", pickle_result
        else:
            logging.error("Host[{host}],CMD={cmd},返回异常=========Start\n{result}\n=========END".format(
                host=host, cmd=cmd, result="\n".join(return_line_list))
            )
            return TechFailKeyError(error_code=ErrorCode.E_PICKLE_DECODE, target_vm=host), None
