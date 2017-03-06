import logging
import base64
import pickle
import traceback


class PickleForSsh:
    __code__ = 'latin1'

    @classmethod
    def deep_copy(cls, obj):
        thing = cls.dumps_to_str(obj)
        new_obj = cls.loads_from_str(thing)

        if obj is new_obj:
            return obj
        else:
            return new_obj

    @classmethod
    def dumps_to_str(cls, obj):
        try:
            return str(base64.standard_b64encode(pickle.dumps(obj)), encoding=cls.__code__)
        except Exception as e:
            logging.error("Pickle Error! Data: {}".format(str(obj)))
            logging.warning(e)
            raise

    @classmethod
    def loads_from_str(cls, things):

        if not things:
            logging.warning("No data to decode")
            return

        if isinstance(things, str):
            try:
                return pickle.loads(base64.standard_b64decode(bytes(things, encoding=cls.__code__)))
            except Exception as e:
                logging.error("Base64 Format Error! Error data: {}".format(things))
                logging.error(traceback.format_exc())
                return

        elif isinstance(things, bytes):
            try:
                return pickle.loads(base64.standard_b64decode(things))
            except BaseException:
                logging.error('Unpickle error:{}'.format(things))
                logging.error(traceback.format_exc())
                return

        else:
            logging.warning(
                "Decode unknown type data to Object happened exception, type={}, Data={}".format(
                    str(type(things)), str(things))
            )
        return
