
# Walle

Walle is a high performance distributed command runner. You can run differen command on hosts you specified with a best feeling you never experienced.


# Nonblock runner

For example, you want to run ``commandA on host1, host2`` and ``run commandB on host3, host4``.

Normally, the execution sequence is as follows.

```
commandA on host1
	|
commandA on host2
	|
commandB on host3
	|
commandB on host4
```

It's synchronized and every new command is blocked by the previous command.
The total consuming time is the sum of all the four command's execution time. That cost a lot!

There is a new way to run these commands in walle.

Walle will create a new coroutine to run every tuple (command, host), for example running commandA on host1 is an individual tuple.

As we momentioned, it will create 4 coroutines and the same commands will be wrapped by a new thread.


* Thread1
	* coroutine1 for ``commandA on host1``
	* coroutine2 for ``commandA on host2``
* Thread2
	* coroutine3 for ``commandA on host1``
	* coroutine4 for ``commandA on host1``

All the coroutines are running asynchronized thanks to the help of the great python3 module **asyncio**

You can find out more detail in **``walle/basic/rpc/my_async_ssh.py``** if you are interested.
There are some essential snippets of the nonblock system as following.

```
class MyAsyncSsh(metaclass=Singleton):
	...
	...
	...

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
	 	...
	 	...
	 	...

    async def run_client(self, host, command, shell=None, use_shell=False, **kwargs):
		...
		...
		...

```


# How to use
* define you own service command,  for example ``wall/common/example/demo.py``

```
class ExampleService:
    @classmethod
    def example_func(cls, msg):
        msg = msg or "No msg"
        response_msg = "{msg} Received!".format(msg=msg)
        return response_msg

```

* pass the params to the ``rpc.call_vms_by_list``


```
call = ExampleService.example_func
call_kwargs = dict(msg="ping")
vms =[you_remote_host1, your_remote_host2]
return_obj = rpc.call_vms_by_list(
    call=call,
    call_kwargs=call_kwargs,
    vms=vms,
)

```