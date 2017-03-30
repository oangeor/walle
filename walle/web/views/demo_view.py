from walle.basic.service_client.base_client import BaseClient


class WalleDemoView():

    def get(self, *args, **kwargs):
        # TODO: 以flask 为例 自己可以修改成自己喜欢的框架

        return self.call_walle()

    def call_walle(self):
        BaseClient.call_vm()
