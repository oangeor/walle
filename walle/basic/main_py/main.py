import sys
import os
import logging
import traceback
import argparse

try:
    root_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir))
    root_path = root_path.split("/walle/walle")[0]
    root_path = os.path.join(root_path, 'walle')

    sys.path.insert(0, root_path)
    # sys.path.insert(0, external_packages_path)
except BaseException:
    print(traceback.format_exc())
    print("Load dependency failed")
    raise

from walle.basic.env_manager import env_mng


class MainEntry:

    def __init__(self):
        self.Entries = {
            "agent": dict(func=self.do_rpc),
            "cmdline": dict(func=self.do_op),
        }

    # @staticmethod
    # def
    @staticmethod
    def do_rpc(*args):
        pass
        # from walle.basic.rpc

    @staticmethod
    def do_op(*args):
        pass

    @staticmethod
    def check_user(allow_user=None):
        '''
        :param allow_user:
        :return: None to allow or raise Exception for forbiddening
        '''
        return

    def do(self, mode, *args):
        try:
            func_conf = self.Entries[mode]

            # Todo
            # self.check_user
            func_conf['func'](*args)
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
            sys.exit(1)

    def parse_config(self, cmdLine):
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mode", help="启动模式", choices=self.Entries.keys(), default='cmdline')
        parser.add_argument("--debug", action="store_true", help="开启debug 日志", default=False)
        parser.add_argument("pargs", nargs="*", metavar="function_args", help="其他参数")
        return parser.parse_args(cmdLine)


def main():
    main_entry = MainEntry()
    configs = main_entry.parse_config(sys.argv[1:])
    # TODO: config Env
    # TODO: debug module
    main_entry.do(configs.mode, *configs.pargs)


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        print(traceback.format_exc())
