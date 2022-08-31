import requests
from testbase import logger

from src.polaris_test_lib.common_lib import CommonLib


class PolarisServer(CommonLib):
    NAMESPACE_PATH = '/naming/v1/namespaces'
    DELETE_NAMESPACE_PATH = NAMESPACE_PATH + '/delete'
    LOGIN_PATH = '/core/v1/user/login'
    INSTANCE_PATH = '/naming/v1/instances'
    DELETE_INSTANCE_PATH = INSTANCE_PATH + '/delete'
    SERVICE_PATH = '/naming/v1/services'
    DELETE_SERVICE_PATH = SERVICE_PATH + '/delete'

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

    def describe_namespace(self, url, limit, offset, namespace_name=None):
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

    def create_service(self, url, create_service_request):
        create_service_requests = self._check_list(create_service_request)
        rsp = self.post(url, json=create_service_requests, headers=self.headers)
        return rsp

    def describe_service(self, url, limit, offset, namespace_name=None, service_name=None, host=None, department=None,
                         business=None, key=None, value=None):
        if any([key, value]):
            if not all([key, value]):
                raise Exception("You must assign both key and value.")

        req = self._format_params(limit=limit, offset=offset, namespace=namespace_name, name=service_name,
                                  host=host, department=department, business=business, keys=key, values=value)
        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def delete_service(self, url, delete_service_request):
        delete_service_requests = self._check_list(delete_service_request)
        rsp = self.post(url, json=delete_service_requests, headers=self.headers)
        return rsp

    def create_service_instance(self, url, create_service_instance_request):
        create_service_instance_requests = self._check_list(create_service_instance_request)
        rsp = self.post(url, json=create_service_instance_requests, headers=self.headers)
        return rsp

    def describe_service_instance(self, url, limit, offset, namespace_name, service_name, host=None, protocol=None,
                                  version=None, healthy=None, isolate=None, key=None, value=None):
        if any([key, value]):
            if not all([key, value]):
                raise Exception("You must assign both key and value.")

        req = self._format_params(limit=limit, offset=offset, namespace=namespace_name, service=service_name,
                                  host=host, protocol=protocol, version=version, healthy=healthy, isolate=isolate,
                                  keys=key, values=value)

        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def delete_service_instance(self, url, delete_service_instance_request):
        delete_service_instance_requests = self._check_list(delete_service_instance_request)
        rsp = self.post(url, json=delete_service_instance_requests, headers=self.headers)
        return rsp
