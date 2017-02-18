import os


def get_env_cls():
    if True:
        from walle.basic.env_manager.default import DefaultEnv as EnvCls
    else:
        from walle.basic.env_manager.product import ProductEnv as EnvCls

    return EnvCls


env_mng = get_env_cls()

if __name__ == "__main__":
    print("env type: ", env_mng.env_type)
