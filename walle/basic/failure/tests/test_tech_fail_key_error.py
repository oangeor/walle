import unittest
from walle.basic.failure.tech_fail_key_error import ErrorCode, TechFailKeyError


class TestTechFailKeyError(unittest.TestCase):
    def test_error_code(self):
        error_code = ErrorCode(ErrorCode.E_RPC_SSH_CONNECT)
        self.assertEqual(error_code.name, "E_RPC_SSH_CONNECT")

    def test_tech_fail_key_error(self):
        tech_fail_key_error = TechFailKeyError(error_code=ErrorCode.E_PICKLE_DECODE, target_vm="127.0.0.1")
        self.assertEqual(tech_fail_key_error.error_code, ErrorCode.E_PICKLE_DECODE.name)

        tech_fail_key_error.error_code = ErrorCode.E_PICKLE_ENCODE.name
        self.assertEqual(tech_fail_key_error.error_code, ErrorCode.E_PICKLE_ENCODE.name)
