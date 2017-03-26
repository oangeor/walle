from enum import Enum
import os


class EnvType(Enum):
    localhost = 0
    prod = 1


class DefaultEnv():
    env_type = EnvType.localhost
    hostname = os.popen("hostname").read()[:-1]
    rpc_timeout = 60

    renice = True
    python3_path = "python3"

    def is_in_prod(self):
        return self.env_type == EnvType.prod

    def is_in_local(self):
        return False
        # return self.env_type == EnvType.localhost
