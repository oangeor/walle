from enum import Enum


class ProblemType(Enum):
    success = 0
    rpc_timeout = 1
    rpc_error = 2

    @staticmethod
    def get_enum_item_by_int(i):
        """根据int值找枚举项"""
        for type in ProblemType:
            if type.value == i:
                return type

    def __str__(self):
        return self.name


if __name__ == '__main__':
    print(ProblemType.success)
    print(ProblemType.os_error.name == "os_error")
