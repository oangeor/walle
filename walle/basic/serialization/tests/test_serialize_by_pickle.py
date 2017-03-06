import unittest

from walle.basic.failure.tech_fail_key_error import ErrorCode
from walle.basic.serialization.serialize_by_pickle import PickleForSsh
from walle.basic.failure.tech_fail_key_error import TechFailKeyError


class TestPickle(unittest.TestCase):
    def test_obj_to_str_and_return_to_obj_and_compare(self):
        obj_original = TechFailKeyError(error_code=ErrorCode.E_RPC_SSH_CONNECT, target_vm="127.0.0.1")
        str_result = PickleForSsh.dumps_to_str(obj_original)
        obj_pickled = PickleForSsh.loads_from_str(str_result)
        self.assertEqual(type(obj_pickled), TechFailKeyError)
        self.assertEqual(obj_pickled.error_code, ErrorCode.E_RPC_SSH_CONNECT.name)
