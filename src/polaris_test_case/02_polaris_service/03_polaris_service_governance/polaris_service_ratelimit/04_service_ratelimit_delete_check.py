import random
import string

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceRatelimitDeleteCheck(PolarisTestCase):
    """
    Used to test delete service ratelimit rule.

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
        self.start_step("Create local service ratelimit rule %s to limit service %s in %s, status disable." % (
            self.ratelimit_rule_name, self.service_name, self.namespace_name))

        self.create_service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_RATELIMIT_PATH

        _kwargs = {"url": self.create_service_ratelimit_rule_url, "rule_name": self.ratelimit_rule_name,
                   "rule_type": "LOCAL", "ratelimit_namespace": self.namespace_name,
                   "ratelimit_service": self.service_name,
                   "ratelimit_method": {"value": "AutoTestPolarisRatelimitMethod", "type": "EXACT",
                                        "value_type": "TEXT"},
                   "ratelimit_arguments": [
                       {"type": "CUSTOM", "key": "AutoTestPolarisRatelimitKey",
                        "value": {"type": "EXACT", "value": "AutoTestPolarisRatelimitValue"}}],
                   "ratelimit_amounts": [{"maxAmount": 1, "validDuration": "1s"}],
                   "ratelimit_regex_combine": True,
                   "ratelimit_action": "REJECT",
                   "failover": "FAILOVER_LOCAL",
                   "disable": True
                   }
        rsp = self.polaris_server.create_service_ratelimit_rule(**_kwargs)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service_ratelimit_rule = rsp.json()["responses"][0].get("rateLimit", None)
        if return_service_ratelimit_rule is None:
            self.fail("Fail! No return except polaris service ratelimit rule.")
        else:
            re_srv_ratelimit_rule_id = return_service_ratelimit_rule.get("id", None)
        # ===========================
        self.start_step("delete rule.")
        self.delete_service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.DELETE_SERVICE_RATELIMIT_PATH
        self.polaris_server.delete_service_ratelimit_rule(url=self.delete_service_ratelimit_rule_url,
                                                          rule_id=re_srv_ratelimit_rule_id)
        # ===========================
        self.start_step("Describe all service ratelimit rules to check delete result.")
        rsp = self.polaris_server.describe_service_ratelimit_rule(url=self.create_service_ratelimit_rule_url,
                                                                  limit=20, offset=0, brief=True)

        ratelimit_rules = rsp.json().get("rateLimits", None)
        if len(ratelimit_rules) == 0:
            self.log_info("Delete service ratelimit rules success.")
            return True

        for ratelimit_rule in ratelimit_rules:
            self.log_info("check service ratelimit rule: %s:%s in %s:%s" % (
                ratelimit_rule["name"], ratelimit_rule["id"], ratelimit_rule["service"], ratelimit_rule["namespace"]))
            self.assert_("Fail! Deleted polaris service ratelimit rule still exist.",
                         self.ratelimit_rule_name != ratelimit_rule["name"])
            self.assert_("Fail! Deleted polaris service ratelimit rule still exist.",
                         re_srv_ratelimit_rule_id != ratelimit_rule["id"])

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, namespace_names=[self.namespace_name])


if __name__ == '__main__':
    ServiceRatelimitDeleteCheck().debug_run()
