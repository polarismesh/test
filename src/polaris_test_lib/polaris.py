import requests
from testbase import logger

from src.polaris_test_lib.common_lib import CommonLib


class PolarisServer(CommonLib):

    NAMESPACE_PATH = '/naming/v1/namespaces'
    DELETE_NAMESPACE_PATH = NAMESPACE_PATH + '/delete'
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
        logger.debug("<<< RE CONTENT  %s\n" % rsp.content)
        return rsp

    @classmethod
    def get(cls, url, params=None, **kwargs):
        logger.debug(">>> GET  %s  %s" % (url, params))
        rsp = requests.get(url, params=params, **kwargs)
        logger.debug("<<< RE HEADERS  %s" % rsp.headers)
        logger.debug("<<< RE  STATUS  %s" % rsp.status_code)
        logger.debug("<<< RE CONTENT  %s\n" % rsp.content)
        return rsp

    @classmethod
    def put(cls, url, data=None, json=None, **kwargs):
        req = data if data is not None else json
        logger.debug(">>> PUT  %s  %s" % (url, req))
        rsp = requests.put(url, data=data, json=json, **kwargs)
        logger.debug("<<< RE HEADERS  %s" % rsp.headers)
        logger.debug("<<< RE  STATUS  %s" % rsp.status_code)
        logger.debug("<<< RE CONTENT  %s\n" % rsp.content)
        return rsp

    @classmethod
    def delete(cls, url, data=None, json=None, **kwargs):
        req = data if data is not None else json
        logger.debug(">>> DELETE  %s  %s" % (url, req))
        rsp = requests.delete(url, data=data, json=json, **kwargs)
        logger.debug("<<< RE HEADERS  %s" % rsp.headers)
        logger.debug("<<< RE  STATUS  %s" % rsp.status_code)
        logger.debug("<<< RE CONTENT  %s\n" % rsp.content)
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

    def describe_namespace(self, url, limit=10, offset=0, namespace_name=None):

        req = self._format_params(limit=limit, offset=offset, name=namespace_name)
        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def modify_namespace(self, url, modify_namespace_request):

        modify_namespace_requests = self._check_list(modify_namespace_request)
        rsp = self.put(url, json=modify_namespace_requests, headers=self.headers)
        return rsp

    def delete_namespace(self, url, delete_namespace_request):

        delete_namespace_requests = self._check_list(delete_namespace_request)
        rsp = self.post(url, json=delete_namespace_requests, headers=self.headers)
        return rsp


