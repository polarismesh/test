import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceAliasCreateCheck(PolarisTestCase):
    """
    Used to test creating service alias.

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
        self.create_single_namespace(self.polaris_server, namespace_name=self.namespace_name)
        self.create_single_namespace(self.polaris_server, namespace_name=self.alias_namespace_name)
        # ===========================
        self.service_name = "AutoTestPolarisServiceAliasService-" + _random_str
        self.create_single_service(self.polaris_server, self.service_name, self.namespace_name)
        # ===========================
        self.service_alias_name = "AutoTestPolarisServiceAlias-" + _random_str
        self.start_step("Check create service alias %s in %s point to service %s in %s." % (
            self.service_alias_name, self.alias_namespace_name, self.service_name, self.namespace_name))

        self.create_service_alias_url = "http://" + self.polaris_console_addr + PolarisServer.SERVICE_ALIAS_PATH
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        rsp = self.polaris_server.create_service_alias(self.create_service_alias_url, self.service_name,
                                                       self.namespace_name,
                                                       self.service_alias_name, self.alias_namespace_name,
                                                       comment="Auto test create polaris service %s" % now)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service_alias = rsp.json()["responses"].get("alias", None)
        if return_service_alias is None:
            self.fail("Fail! No return except polaris service alias .")
        else:
            re_srv_alias_name = rsp.json()["responses"].get("alias", None)
            re_srv_alias_namespace_name = rsp.json()["responses"].get("alias_namespace", None)

            self.assert_("Fail! No return except polaris service alias name.",
                         re_srv_alias_name == self.service_alias_name)
            self.assert_("Fail! No return except polaris service alias namespace name.",
                         re_srv_alias_namespace_name == self.alias_namespace_name)

        if self.test_result.passed:
            self.log_info("Success to check return service alias and polaris code!")

        service_aliases = self.get_all_service_aliases(self.polaris_server)
        for service_alias in service_aliases:
            if service_alias["alias"] == self.service_alias_name:
                self.assert_("Fail! No return except polaris service alias namespace.",
                             service_alias["alias_namespace"] == self.alias_namespace_name)
                self.assert_("Fail! No return except polaris service alias point to service.",
                             service_alias["service"] == self.service_name)
                self.assert_("Fail! No return except polaris service alias point to service namespace.",
                             service_alias["namespace"] == self.namespace_name)
                break
        else:
            self.fail("Fail! No return except polaris service alias.")

        if self.test_result.passed:
            self.log_info("Success to check return service alias and polaris code!")

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, self.namespace_name)
        self.clean_test_namespaces(self.polaris_server, self.alias_namespace_name)


if __name__ == '__main__':
    ServiceAliasCreateCheck().debug_run()
