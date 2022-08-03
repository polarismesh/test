import requests
from testbase import logger


class POLARIS_SERVER:

    def __init__(self):
        pass

    @classmethod
    def _format_params(cls, **kwargs):
        req = {}
        for key, value in kwargs.items():
            if value is not None:
                req.update({key: value})
        return req

    @classmethod
    def get_initial_token(cls, url, username, password, owner="polaris"):

        req = cls._format_params(name=username, password=password, owner=owner)
        logger.debug(">>> post  %s  %s" % (url, req))
        rsp = requests.post(url, json=req)

        logger.debug("<<< return headers  %s" % rsp.headers)
        logger.debug("<<< return status  %s" % rsp.status_code)
        logger.debug("<<< return content  %s" % rsp.content)
        return rsp
