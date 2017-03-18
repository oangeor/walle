from walle.basic.main_py.singleton import Singleton
import asyncio
import threading
import asyncssh
import os
import logging
import traceback


class MyAsyncSsh(metaclass=Singleton):
    def __init__(self, key_files=('~/.ssh/id_rsa',), username='log'):
        self.key_files = key_files
        self.keys = None
        self.conn_cache = dict()
        self.username = username
        self.loop = asyncio.new_event_loop()
        self.t = None  # thread

    @staticmethod
    def _async_thread(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def _ensure_loop_thread(self):
        if self.t and self.t.is_alive():
            return
        self.t = threading.Thread(target=self._async_thread, args=(self.loop,))
        self.t.daemon = True
        self.t.start()

    def run_command_on_hosts(self, hosts, cmd, timeout=None, **kwargs):
        self._ensure_loop_thread()
        try:
            future = asyncio.run_coroutine_threadsafe(self.run_multiple_clients(hosts, cmd, **kwargs), self.loop)
            result = future.result(timeout=timeout)
            return result
        except BaseException:
            logging.error(traceback.format_exc())
            return {h: '' for h in hosts}

    async def run_multiple_clients(self, hosts, cmd, **kwargs):
        # await self.
        tasks = (self.run_client(host, cmd, **kwargs) for host in hosts)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        try:
            return dict(results)
        except TypeError as e:
            logging.error("Call ({cmd}) on [{h}] failed: (result={r}, {e})".format(r=results, e=e, h=hosts, cmd=cmd))
            return {h: '' for h in hosts}

    async def run_client(self, host, command, shell=None, use_shell=False, **kwargs):
        try:
            conn, _ = await self.get_conn(host)
        except asyncssh.DisconnectError as e:
            logging.error("SSH1 Connect to {} lost:{}".format(host, str(e)))
            try:
                conn.close()

            except BaseException:
                pass
            self.conn_cache.pop(host)
            try:
                conn, _ = await self.get_conn(host)

            except Exception as e:
                logging.error("SSH2 Reconnect to{} failed:{}".format(host, str(e)))
                return host, e
        except Exception as e:
            logging.error("SSH3 Connect to {} failed:{}".format(host, str(e)))
            return host, e

        # parse command
        for _char in ['\\', '"', '$', '`']:
            command = command.replace(_char, '\%s' % (_char,))
        shell = '$SHELL -c' if not shell else shell
        _command = '%s "%s"' % (shell, command,) if use_shell else command
        return host, await conn.run(_command)

    def get_keys(self):
        if not self.keys:
            try:
                self.keys = [asyncssh.read_private_key(os.path.expanduser(f)) for f in self.key_files if
                             os.path.exists(os.path.expanduser(f))]
            except BaseException:
                return ()
        return self.keys

    def get_conn(self, host):
        try:
            return self.conn_cache[host]
        except KeyError:
            self.conn_cache[host] = asyncio.ensure_future(
                asyncssh.create_connection(
                    None,
                    host,
                    username=self.username,
                    known_hosts=None,
                    client_keys=self.get_keys(),
                )
            )
            return self.conn_cache[host]
