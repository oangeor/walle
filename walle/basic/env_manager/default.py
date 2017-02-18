from enum import Enum


class EnvType(Enum):
    localhost = 0
    prod = 1


class DefaultEnv():
    env_type = EnvType.localhost

    def is_in_prod(self):
        return self.env_type == EnvType.prod

    def is_in_local(self):
        return self.env_type == EnvType.localhost
