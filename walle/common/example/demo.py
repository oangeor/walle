class ExampleService:

    @classmethod
    def example_func(cls, msg):
        msg = msg or "No msg"
        response_msg = "{msg}Received!".format(msg=msg)
        return response_msg
