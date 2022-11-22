import requests
from testbase import logger

from src.polaris_test_lib.common_lib import CommonLib


class PolarisServer(CommonLib):
    LOGIN_PATH = '/core/v1/user/login'

    NAMESPACE_PATH = '/naming/v1/namespaces'
    DELETE_NAMESPACE_PATH = NAMESPACE_PATH + '/delete'

    INSTANCE_PATH = '/naming/v1/instances'
    DELETE_INSTANCE_PATH = INSTANCE_PATH + '/delete'

    SERVICE_PATH = '/naming/v1/services'
    DELETE_SERVICE_PATH = SERVICE_PATH + '/delete'

    SERVICE_ALIAS_PATH = '/naming/v1/service/alias'
    DESCRIBE_SERVICE_ALIAS_PATH = '/naming/v1/service/aliases'
    DELETE_SERVICE_ALIAS_PATH = DESCRIBE_SERVICE_ALIAS_PATH + '/delete'

    EUREKA_REGISTER_PATH = "/eureka/apps/{app_id}"

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

    def modify_service(self, url, modify_service_request):
        modify_service_requests = self._check_list(modify_service_request)
        rsp = self.put(url, json=modify_service_requests, headers=self.headers)
        return rsp

    def delete_service(self, url, delete_service_request):
        delete_service_requests = self._check_list(delete_service_request)
        rsp = self.post(url, json=delete_service_requests, headers=self.headers)
        return rsp

    def create_service_alias(self, url, create_service_alias_request):
        create_service_alias_requests = self._check_list(create_service_alias_request)
        rsp = self.post(url, json=create_service_alias_requests, headers=self.headers)
        return rsp

    def describe_service_alias(self, url, limit, offset, alias_namespace_name=None, point_to_service_name=None):

        req = self._format_params(limit=limit, offset=offset, alias_namespace=alias_namespace_name,
                                  service=point_to_service_name)
        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def modify_service_alias(self, url, modify_service_request):
        modify_service_requests = self._check_list(modify_service_request)
        rsp = self.put(url, json=modify_service_requests, headers=self.headers)
        return rsp

    def delete_service_alias(self, url, delete_service_alias_request):
        delete_service_alias_requests = self._check_list(delete_service_alias_request)
        rsp = self.post(url, json=delete_service_alias_requests, headers=self.headers)
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

    def eureka_register_service(self, url, host, app, ip, vip, secure_vip, status, port, secure_port, home_page_url,
                                status_page_url, health_check_url, data_center_info, lease_info, metadata):
        req = {
            "instance": self._format_params(hostName=host, app=app, ipAddr=ip, vipAddress=vip,
                                            secureVipAddress=secure_vip, status=status, port=port,
                                            securePort=secure_port, homePageUrl=home_page_url,
                                            statusPageUrl=status_page_url, healthCheckUrl=health_check_url,
                                            dataCenterInfo=data_center_info, leaseInfo=lease_info, metadata=metadata)
        }
        url = url.format(app_id=app)
        logger.info(url)
        rsp = self.post(url, json=req, headers=self.headers)
        return rsp
