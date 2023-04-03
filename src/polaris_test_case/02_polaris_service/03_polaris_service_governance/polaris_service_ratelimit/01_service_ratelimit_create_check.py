import random
import string

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceRatelimitCreateCheck(PolarisTestCase):
    """
    Used to test creating service ratelimit rule.

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
        self.namespace_name = "AutoTestPolarisRatelimitNamespace-" + _random_str
        self.service_name = "AutoTestPolarisRatelimitService-" + _random_str

        self.create_single_namespace(self.polaris_server, namespace_name=self.namespace_name)
        self.create_single_service(self.polaris_server, self.service_name, self.namespace_name)

        self.ratelimit_rule_name = "AutoTestPolarisRatelimit-" + _random_str

        # ===========================
        self.start_step("Create local service ratelimit rule %s to limit service %s in %s." % (
            self.ratelimit_rule_name, self.service_name, self.namespace_name))

        self.create_service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_RATELIMIT_PATH

        srv_ratelimit_rule_failover = "FAILOVER_LOCAL"
        srv_ratelimit_rule_type = "LOCAL"
        rsp = self.polaris_server.create_service_ratelimit_rule(
            self.create_service_ratelimit_rule_url, self.ratelimit_rule_name, rule_type="LOCAL",
            ratelimit_namespace=self.namespace_name, ratelimit_service=self.service_name,
            ratelimit_method={"value": "AutoTestPolarisRatelimitMethod", "type": "EXACT"},
            ratelimit_arguments=[{"type": "CUSTOM",
                                  "key": "AutoTestPolarisRatelimitKey",
                                  "value": {"type": "EXACT", "value": "AutoTestPolarisRatelimitValue"}}],
            ratelimit_amounts=[{"maxAmount": 1, "validDuration": "1s"}],
            ratelimit_regex_combine=True, ratelimit_action="REJECT", failover=srv_ratelimit_rule_failover, disable=True)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        return_service_ratelimit_rule = rsp.json()["responses"][0].get("rateLimit", None)
        if return_service_ratelimit_rule is None:
            self.fail("Fail! No return except polaris service ratelimit rule .")
        else:
            re_srv_ratelimit_rule_failover = return_service_ratelimit_rule.get("failover", None)
            # re_srv_ratelimit_rule_id = return_service_ratelimit_rule.get("id", None)
            re_srv_ratelimit_rule_name = return_service_ratelimit_rule.get("name", None)
            re_srv_ratelimit_rule_namespace = return_service_ratelimit_rule.get("namespace", None)
            re_srv_ratelimit_rule_service = return_service_ratelimit_rule.get("service", None)
            re_srv_ratelimit_rule_type = return_service_ratelimit_rule.get("type", None)

            self.assert_("Fail! No return except polaris service ratelimit rule name.",
                         re_srv_ratelimit_rule_name == self.ratelimit_rule_name)
            self.assert_("Fail! No return except polaris service ratelimit rule failover.",
                         re_srv_ratelimit_rule_failover == srv_ratelimit_rule_failover)
            self.assert_("Fail! No return except polaris service ratelimit rule namespace.",
                         re_srv_ratelimit_rule_namespace == self.namespace_name)
            self.assert_("Fail! No return except polaris service ratelimit rule namespace.",
                         re_srv_ratelimit_rule_service == self.service_name)
            self.assert_("Fail! No return except polaris service ratelimit rule type.",
                         re_srv_ratelimit_rule_type == srv_ratelimit_rule_type)

        if self.test_result.passed:
            self.log_info("Success to check return service ratelimit rule and polaris code!")

    def post_test(self):
        self.clean_test_services(self.polaris_server, namespace_name=self.namespace_name, service_name=self.service_name)

if __name__ == '__main__':
    ServiceRatelimitCreateCheck().debug_run()
