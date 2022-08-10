import requests
from testbase import logger

from src.polaris_test_lib.common_lib import CommonLib


class PolarisServer(CommonLib):

    CREATE_NAMESPACE_PATH = '/naming/v1/namespaces'
    DELETE_NAMESPACE_PATH = '/naming/v1/namespaces/delete'
    LOGIN_PATH = '/core/v1/user/login'

    def __init__(self, auth_token, auth_user_id):
        self.headers = {"X-Polaris-Token": auth_token, "X-Polaris-User": auth_user_id}

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        req = data if data is not None else json
        logger.debug(">>> POST  %s  %s" % (url, req))
        rsp = requests.post(url, data=data, json=json, **kwargs)
        logger.debug("<<< RE HEADERS  %s" % rsp.headers)
        logger.debug("<<< RE  STATUS  %s" % rsp.status_code)
        logger.debug("<<< RE CONTENT  %s" % rsp.content)
        return rsp

    @classmethod
    def delete(cls, url, data=None, json=None, **kwargs):
        req = data if data is not None else json
        logger.debug(">>> DELETE  %s  %s" % (url, req))
        rsp = requests.delete(url, data=data, json=json, **kwargs)
        logger.debug("<<< RE HEADERS  %s" % rsp.headers)
        logger.debug("<<< RE  STATUS  %s" % rsp.status_code)
        logger.debug("<<< RE CONTENT  %s" % rsp.content)
        return rsp

    @classmethod
    def get_initial_token(cls, url, username, password, owner="polaris"):

        req = cls._format_params(name=username, password=password, owner=owner)
        rsp = cls.post(url, json=req)
        return rsp

    def create_namespace(self, url, create_namespace_request):

        create_namespace_requests = self._check_list(create_namespace_request)
        rsp = self.post(url, json=create_namespace_requests, headers=self.headers)
        return rsp

    def delete_namespace(self, url, delete_namespace_request):

        delete_namespace_requests = self._check_list(delete_namespace_request)
        rsp = self.post(url, json=delete_namespace_requests, headers=self.headers)
        return rsp


