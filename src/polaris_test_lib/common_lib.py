import random
import os
os.system("pip3 install faker")
from faker import Faker


class CommonLib:
    @classmethod
    def _format_params(cls, **kwargs):
        req = {}
        for key, value in kwargs.items():
            if value is not None:
                req.update({key: value})
        return req

    @classmethod
    def _check_list(cls, param):

        convert_param = []
        if param is None:
            param = []
        elif type(param) != list:
            if callable(getattr(param, "get_dict", None)):
                convert_param = [param.get_dict()]
            else:
                param = [param]
        elif type(param) == list:
            for p in param:
                if callable(getattr(p, "get_dict", None)):
                    convert_param.append(p.get_dict())
        return convert_param if convert_param != [] else param

    @classmethod
    def _random_ip(cls):

        import random
        import socket
        import struct

        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    @classmethod
    def _random_num(cls):
        return random.randint(100000, 999999)

    @classmethod
    def _random_phone_num(cls):
        fake = Faker(locale='zh_CN')
        return fake.phone_number()

    @classmethod
    def _random_email(cls):
        fake = Faker(locale='zh_CN')
        return fake.safe_email()
