import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceAliasModifyCheck(PolarisTestCase):
    """
    Used to test modify service alias.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        # ===========================
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.namespace_name = "AutoTestPolarisServiceAliasNamespace-" + _random_str
        self.alias_namespace_name = "AutoTestPolarisServiceAliasNamespace2-" + _random_str
        self.service_name = "AutoTestPolarisServiceAliasService-" + _random_str
        self.service_name2 = "AutoTestPolarisServiceAliasService2-" + _random_str
        self.service_alias_name = "AutoTestPolarisServiceAlias-" + _random_str

        self.create_single_namespace(self.polaris_server, namespace_name=self.namespace_name)
        self.create_single_namespace(self.polaris_server, namespace_name=self.alias_namespace_name)
        self.create_single_service(self.polaris_server, self.service_name, self.namespace_name)
        self.create_single_service(self.polaris_server, self.service_name2, self.namespace_name)
        # ===========================
        # alias-1
        self.create_single_service_alias(polaris_server=self.polaris_server, service_name=self.service_name,
                                         namespace_name=self.namespace_name, service_alias_name=self.service_alias_name,
                                         alias_namespace_name=self.alias_namespace_name)

        # ===========================
        time.sleep(2)
        self.start_step("Modify polaris service alias comment.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test update polaris service alias %s" % now
        self.modify_service_alias_url = self.create_service_alias_url
        rsp = self.polaris_server.modify_service_alias(self.modify_service_alias_url, alias=self.service_alias_name,
                                                       alias_namespace=self.alias_namespace_name, comment=comment,
                                                       service_name=self.service_name,
                                                       namespace_name=self.namespace_name)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_srv_alias = rsp.json().get("alias", None)
        if return_srv_alias is None:
            self.fail("Fail! No return except polaris service alias.")
            return
        else:
            re_srv_alias_name = return_srv_alias.get("alias", None)
            self.assert_("Fail! No return except polaris service alias", re_srv_alias_name == self.service_alias_name)
            re_srv_alias_comment = return_srv_alias.get("comment", None)
            self.assert_("Fail! No return except polaris service alias comment.", re_srv_alias_comment == comment)
            re_srv_alias_point_to_srv = return_srv_alias.get("service", None)
            self.assert_("Fail! No return except polaris service alias point to service.",
                         re_srv_alias_point_to_srv == self.service_name)
            re_srv_alias_point_to_srv_ns = return_srv_alias.get("namespace", None)
            self.assert_("Fail! No return except polaris service alias point to service namespace.",
                         re_srv_alias_point_to_srv_ns == self.namespace_name)

        if self.test_result.passed:
            self.log_info("Success to check return namespace and polaris code!")

        # ===========================
        time.sleep(2)
        self.start_step("Modify polaris service alias point to service.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test update polaris service alias %s" % now
        self.modify_service_alias_url = self.create_service_alias_url
        rsp = self.polaris_server.modify_service_alias(self.modify_service_alias_url, alias=self.service_alias_name,
                                                       alias_namespace=self.alias_namespace_name, comment=comment,
                                                       service_name=self.service_name2,
                                                       namespace_name=self.namespace_name)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_srv_alias = rsp.json().get("alias", None)
        if return_srv_alias is None:
            self.fail("Fail! No return except polaris service alias.")
            return
        else:
            re_srv_alias_name = return_srv_alias.get("alias", None)
            self.assert_("Fail! No return except polaris service alias", re_srv_alias_name == self.service_alias_name)
            re_srv_alias_comment = return_srv_alias.get("comment", None)
            self.assert_("Fail! No return except polaris service alias comment.", re_srv_alias_comment == comment)
            re_srv_alias_point_to_srv = return_srv_alias.get("service", None)
            self.assert_("Fail! No return except polaris service alias point to service.",
                         re_srv_alias_point_to_srv == self.service_name2)
            re_srv_alias_point_to_srv_ns = return_srv_alias.get("namespace", None)
            self.assert_("Fail! No return except polaris service alias point to service namespace.",
                         re_srv_alias_point_to_srv_ns == self.namespace_name)

        if self.test_result.passed:
            self.log_info("Success to check return namespace and polaris code!")

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name])
        self.clean_test_namespaces(self.polaris_server, [self.alias_namespace_name])


if __name__ == '__main__':
    ServiceAliasModifyCheck().debug_run()
