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

    SERVICE_RATELIMIT_PATH = "/naming/v1/ratelimits"
    DELETE_SERVICE_RATELIMIT_PATH = SERVICE_RATELIMIT_PATH + '/delete'

    EUREKA_REGISTER_PATH = "/eureka/apps"

    USER_PATH = '/core/v1/users'
    DELETE_USER_PATH = USER_PATH + '/delete'
    DESCRIBE_USER_PATH = "/core/v1/user"
    MODIFY_USER_PASSWORD_PATH = DESCRIBE_USER_PATH + '/password'
    VIEW_USER_TOKEN_PATH = DESCRIBE_USER_PATH + '/token'
    REFRESH_USER_TOKEN_PATH = VIEW_USER_TOKEN_PATH + '/refresh'
    OPERATE_USER_TOKEN_PATH = VIEW_USER_TOKEN_PATH + '/status'

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
    def get_initial_token(cls, url, username, password, owner):
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

    def create_service_alias(self, url, service_name, namespace_name, alias_name, alias_namespace_name, comment=None):
        create_service_alias_request = self._format_params(service=service_name, namespace=namespace_name,
                                                           alias=alias_name,
                                                           alias_namespace=alias_namespace_name, comment=comment)
        rsp = self.post(url, json=create_service_alias_request, headers=self.headers)
        return rsp

    def describe_service_alias(self, url, limit, offset, alias_namespace_name=None, point_to_service_name=None):

        req = self._format_params(limit=limit, offset=offset, alias_namespace=alias_namespace_name,
                                  service=point_to_service_name)
        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def modify_service_alias(self, url, alias, alias_namespace, comment=None, service_name=None, namespace_name=None):
        req = self._format_params(alias=alias, alias_namespace=alias_namespace, comment=comment,
                                  service=service_name, namespace=namespace_name)
        rsp = self.put(url, json=req, headers=self.headers)
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
        url = "%s/%s" % (url, app)
        logger.info(url)
        rsp = self.post(url, json=req, headers=self.headers)
        return rsp

    def eureka_describe_service(self, url, app=None, instance_id=None):
        if all([app, instance_id]):
            url = "%s/%s/%s" % (url, app, instance_id)
        elif any([app, instance_id]):
            if app is not None:
                url = "%s/%s" % (url, app)
            if instance_id is not None:
                raise Exception("You must assign at least app or assign both app and instance.")

        logger.info(url)
        rsp = self.get(url, headers=self.headers)
        return rsp

    def create_service_ratelimit_rule(self, url, rule_name, rule_type, ratelimit_namespace, ratelimit_service,
                                      ratelimit_method, ratelimit_arguments, ratelimit_amounts, ratelimit_regex_combine,
                                      ratelimit_action, failover, disable, max_queue_delay=1, resource="QPS"):
        req = self._format_params(name=rule_name, type=rule_type, namespace=ratelimit_namespace,
                                  service=ratelimit_service, method=ratelimit_method, arguments=ratelimit_arguments,
                                  amounts=ratelimit_amounts, regex_combine=ratelimit_regex_combine,
                                  action=ratelimit_action, failover=failover, disable=disable,
                                  max_queue_delay=max_queue_delay, resource=resource)
        rsp = self.post(url, json=[req], headers=self.headers)
        return rsp

    def describe_service_ratelimit_rule(self, url, limit, offset, brief=None, ratelimit_rule_id=None,
                                        ratelimit_rule_name=None, ratelimit_rule_disable=None,
                                        namespace_name=None, service_name=None):
        req = self._format_params(limit=limit, offset=offset, brief=brief, id=ratelimit_rule_id,
                                  name=ratelimit_rule_name, disable=ratelimit_rule_disable, namespace=namespace_name,
                                  service=service_name)
        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def modify_service_ratelimit_rule(self, url, rule_id, rule_name, rule_type, ratelimit_namespace, ratelimit_service,
                                      ratelimit_method, ratelimit_arguments, ratelimit_amounts, ratelimit_regex_combine,
                                      ratelimit_action, failover, disable, max_queue_delay=1, resource="QPS"):
        req = self._format_params(id=rule_id, name=rule_name, type=rule_type, namespace=ratelimit_namespace,
                                  service=ratelimit_service, method=ratelimit_method, arguments=ratelimit_arguments,
                                  amounts=ratelimit_amounts, regex_combine=ratelimit_regex_combine,
                                  action=ratelimit_action, failover=failover, disable=disable,
                                  max_queue_delay=max_queue_delay, resource=resource)
        rsp = self.put(url, json=[req], headers=self.headers)
        return rsp

    def delete_service_ratelimit_rule(self, url, rule_id):
        req = self._format_params(id=rule_id)
        rsp = self.post(url, json=[req], headers=self.headers)
        return rsp

    def create_user(self, url, user_info):
        rsp = self.post(url, json=user_info, headers=self.headers)
        return rsp

    def delete_user(self, url, user_id):
        req = self._format_params(id=user_id)
        rsp = self.post(url, json=[req], headers=self.headers)
        return rsp

    def describe_users(self, url, user_id, limit=10, offset=0, get_by_id=False):
        req = self._format_params(limit=limit, offset=offset)
        if get_by_id:
            req = self._format_params(id=user_id)
        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def modify_user_password(self, url, user_id, new_password, old_password=None):
        req = self._format_params(id=user_id, new_password=new_password, old_password=old_password)
        rsp = self.put(url, json=req, headers=self.headers)
        return rsp

    def modify_user_info(self, url, user_id, mobile=None, email=None, comment=None):
        req = self._format_params(id=user_id, mobile=mobile, email=email, comment=comment)
        rsp = self.put(url, json=req, headers=self.headers)
        return rsp

    def view_user_token(self, url, user_id):
        req = self._format_params(id=user_id)
        rsp = self.get(url, params=req, headers=self.headers)
        return rsp

    def refresh_user_token(self, url, user_id):
        req = self._format_params(id=user_id)
        rsp = self.put(url, json=req, headers=self.headers)
        return rsp

    def operate_user_token(self, url, user_id, token_enable=False):
        req = self._format_params(id=user_id, token_enable=token_enable)
        rsp = self.put(url, json=req, headers=self.headers)
        return rsp
