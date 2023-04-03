import random
import string

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceRatelimitDescribeCheck(PolarisTestCase):
    """
    Used to test describe service ratelimit rule.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def check_return_service_ratelimit_rules(self, check_total, check_size, check_polaris_code,
                                             check_service_ratelimit_rule_names, **kwargs):
        rsp = self.polaris_server.describe_service_ratelimit_rule(**kwargs)

        polaris_code = rsp.json().get("code", None)
        return_rule_total = rsp.json().get("amount", None)
        return_rule_size = rsp.json().get("size", None)

        self.assert_("Fail! No return except polaris code.", polaris_code == check_polaris_code)
        self.assert_("Fail! No return except polaris service ratelimit rule amount.", return_rule_total == check_total)
        self.assert_("Fail! No return except polaris service ratelimit rule size.", return_rule_size == check_size)

        return_rules = rsp.json().get("rateLimits", None)
        rule_names = [rule["name"] for rule in return_rules]
        self.assert_("Fail! No return except polaris service ratelimit rules.",
                     rule_names.sort() == check_service_ratelimit_rule_names.sort())

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        # ===========================
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.namespace_name = "AutoTestPolarisRatelimitNamespace-" + _random_str
        self.service_name = "AutoTestPolarisRatelimitService-" + _random_str
        self.service_name2 = "AutoTestPolarisRatelimitService2-" + _random_str

        self.create_single_namespace(self.polaris_server, namespace_name=self.namespace_name)
        self.create_single_service(self.polaris_server, self.service_name, self.namespace_name)
        self.create_single_service(self.polaris_server, self.service_name2, self.namespace_name)

        self.ratelimit_rule_name = "AutoTestPolarisRatelimit-" + _random_str
        self.ratelimit_rule_name2 = "AutoTestPolarisRatelimit2-" + _random_str

        # ===========================
        self.start_step("Create local service ratelimit rule %s to limit service %s in %s, status disable." % (
            self.ratelimit_rule_name, self.service_name, self.namespace_name))

        self.create_service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_RATELIMIT_PATH

        srv_ratelimit_rule_failover = "FAILOVER_LOCAL"
        srv_ratelimit_rule_type = "LOCAL"
        rsp = self.polaris_server.create_service_ratelimit_rule(
            self.create_service_ratelimit_rule_url, self.ratelimit_rule_name, rule_type=srv_ratelimit_rule_type,
            ratelimit_namespace=self.namespace_name, ratelimit_service=self.service_name,
            ratelimit_method={"value": "AutoTestPolarisRatelimitMethod", "type": "EXACT"},
            ratelimit_arguments=[{"type": "CUSTOM",
                                  "key": "AutoTestPolarisRatelimitKey",
                                  "value": {"type": "EXACT", "value": "AutoTestPolarisRatelimitValue"}}],
            ratelimit_amounts=[{"maxAmount": 1, "validDuration": "1s"}],
            ratelimit_regex_combine=True, ratelimit_action="REJECT", failover=srv_ratelimit_rule_failover, disable=True)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        # ===========================
        self.start_step("Create local service ratelimit rule %s to limit service %s in %s, status enable." % (
            self.ratelimit_rule_name2, self.service_name2, self.namespace_name))

        self.create_service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_RATELIMIT_PATH

        srv_ratelimit_rule_failover = "FAILOVER_LOCAL"
        srv_ratelimit_rule_type = "LOCAL"
        rsp = self.polaris_server.create_service_ratelimit_rule(
            self.create_service_ratelimit_rule_url, self.ratelimit_rule_name2, rule_type=srv_ratelimit_rule_type,
            ratelimit_namespace=self.namespace_name, ratelimit_service=self.service_name2,
            ratelimit_method={"value": "AutoTestPolarisRatelimitMethod", "type": "EXACT"},
            ratelimit_arguments=[{"type": "CUSTOM",
                                  "key": "AutoTestPolarisRatelimitKey",
                                  "value": {"type": "EXACT", "value": "AutoTestPolarisRatelimitValue"}}],
            ratelimit_amounts=[{"maxAmount": 1, "validDuration": "1s"}],
            ratelimit_regex_combine=True, ratelimit_action="REJECT", failover=srv_ratelimit_rule_failover, disable=False)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        self.describe_service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_RATELIMIT_PATH
        _kwargs = {"url": self.describe_service_ratelimit_rule_url, "brief": True, "limit": 10, "offset": 0}

        # ===========================
        self.start_step("Check describe service by rule name.")
        _kwargs.update({"ratelimit_rule_name": self.ratelimit_rule_name})
        self.check_return_service_ratelimit_rules(check_total=1, check_size=1, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[self.ratelimit_rule_name], **_kwargs)

        _kwargs["ratelimit_rule_name"] = "ErrorRuleName"
        self.check_return_service_ratelimit_rules(check_total=0, check_size=0, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[], **_kwargs)

        _kwargs["ratelimit_rule_name"] = _random_str
        self.check_return_service_ratelimit_rules(check_total=2, check_size=2, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[self.ratelimit_rule_name, self.ratelimit_rule_name2], **_kwargs)

        # ===========================
        self.start_step("Check describe service by correct rule name and status.")
        _kwargs.update({"ratelimit_rule_disable": "true"})
        self.check_return_service_ratelimit_rules(check_total=1, check_size=1, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[self.ratelimit_rule_name], **_kwargs)


        _kwargs.update({"ratelimit_rule_disable": "false"})
        self.check_return_service_ratelimit_rules(check_total=1, check_size=1, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[self.ratelimit_rule_name2], **_kwargs)

        # ===========================
        self.start_step("Check describe service by correct rule name, limit namespace.")
        _kwargs.pop("ratelimit_rule_disable")
        _kwargs.update({"namespace_name": self.namespace_name})
        self.check_return_service_ratelimit_rules(check_total=2, check_size=2, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[self.ratelimit_rule_name, self.ratelimit_rule_name2], **_kwargs)

        _kwargs["namespace_name"] = "Polaris"
        self.check_return_service_ratelimit_rules(check_total=0, check_size=0, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[], **_kwargs)

        # ===========================
        self.start_step("Check describe service by correct rule name, limit namespace and limit service.")
        _kwargs["namespace_name"] = self.namespace_name
        _kwargs.update({"service_name": self.service_name})
        self.check_return_service_ratelimit_rules(check_total=1, check_size=1, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[self.ratelimit_rule_name], **_kwargs)

        _kwargs["service_name"] = self.service_name2
        self.check_return_service_ratelimit_rules(check_total=1, check_size=1, check_polaris_code=200000,
                             check_service_ratelimit_rule_names=[self.ratelimit_rule_name2], **_kwargs)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, namespace_names=[self.namespace_name])

if __name__ == '__main__':
    ServiceRatelimitDescribeCheck().debug_run()
