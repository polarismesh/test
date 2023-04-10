import random
import string

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceRatelimitModifyCheck(PolarisTestCase):
    """
    Used to test modify service ratelimit rule.

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
        self.fake_namespace_name = "test-fake-namespace" + _random_str
        self.service_name = "AutoTestPolarisRatelimitService-" + _random_str
        self.fake_service_name = "test-fake-service" + _random_str

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
            self.fail("Fail! No return except polaris service ratelimit rule .")
        else:
            re_srv_ratelimit_rule_id = return_service_ratelimit_rule.get("id", None)
        # ===========================
        self.start_step("update rule status DISABLE to ENABLE.")
        _kwargs.update({"rule_id": re_srv_ratelimit_rule_id})

        _kwargs["disable"] = False

        rsp = self.polaris_server.modify_service_ratelimit_rule(**_kwargs)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service_ratelimit_rule = rsp.json()["responses"][0].get("rateLimit", None)
        if return_service_ratelimit_rule is None:
            self.fail("Fail! No return except polaris service ratelimit rule .")
        else:
            re_srv_ratelimit_rule_status = return_service_ratelimit_rule.get("disable", None)

            self.assert_("Fail! No return except polaris service ratelimit rule status.",
                         re_srv_ratelimit_rule_status == _kwargs["disable"])

        # ===========================
        self.start_step("update rule type LOCAL to GLOBAL, and failover LOCAL to PASS.")
        _kwargs["rule_type"] = "GLOBAL"
        _kwargs["failover"] = "FAILOVER_PASS"

        rsp = self.polaris_server.modify_service_ratelimit_rule(**_kwargs)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service_ratelimit_rule = rsp.json()["responses"][0].get("rateLimit", None)
        if return_service_ratelimit_rule is None:
            self.fail("Fail! No return except polaris service ratelimit rule .")
        else:
            re_srv_ratelimit_rule_status = return_service_ratelimit_rule.get("disable", None)
            re_srv_ratelimit_rule_type = return_service_ratelimit_rule.get("type", None)
            re_srv_ratelimit_rule_failover = return_service_ratelimit_rule.get("failover", None)

            self.assert_("Fail! No return except polaris service ratelimit rule status.",
                         re_srv_ratelimit_rule_status == _kwargs["disable"])
            self.assert_("Fail! No return except polaris service ratelimit rule type.",
                         re_srv_ratelimit_rule_type == _kwargs["rule_type"])
            self.assert_("Fail! No return except polaris service ratelimit rule failover.",
                         re_srv_ratelimit_rule_failover == _kwargs["failover"])

        # ===========================
        self.start_step("update rule type GLOBAL to LOCAL, and action REJECT to UNIRATE.")
        _kwargs["rule_type"] = "LOCAL"
        _kwargs["ratelimit_action"] = "UNIRATE"
        _kwargs.update({"max_queue_delay": 3})

        rsp = self.polaris_server.modify_service_ratelimit_rule(**_kwargs)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service_ratelimit_rule = rsp.json()["responses"][0].get("rateLimit", None)
        if return_service_ratelimit_rule is None:
            self.fail("Fail! No return except polaris service ratelimit rule .")
        else:
            re_srv_ratelimit_rule_status = return_service_ratelimit_rule.get("disable", None)
            re_srv_ratelimit_rule_type = return_service_ratelimit_rule.get("type", None)
            re_srv_ratelimit_rule_failover = return_service_ratelimit_rule.get("failover", None)
            re_srv_ratelimit_rule_action = return_service_ratelimit_rule.get("action", None)
            re_srv_ratelimit_rule_max_queue_delay = return_service_ratelimit_rule.get("max_queue_delay", None)

            self.assert_("Fail! No return except polaris service ratelimit rule status.",
                         re_srv_ratelimit_rule_status == _kwargs["disable"])
            self.assert_("Fail! No return except polaris service ratelimit rule type.",
                         re_srv_ratelimit_rule_type == _kwargs["rule_type"])
            self.assert_("Fail! No return except polaris service ratelimit rule failover.",
                         re_srv_ratelimit_rule_failover == _kwargs["failover"])
            self.assert_("Fail! No return except polaris service ratelimit rule action.",
                         re_srv_ratelimit_rule_action == _kwargs["ratelimit_action"])
            self.assert_("Fail! No return except polaris service ratelimit rule max_queue_delay.",
                         re_srv_ratelimit_rule_max_queue_delay == _kwargs["max_queue_delay"])

        # ===========================
        self.start_step("update rule limit service describe.")
        _kwargs["ratelimit_namespace"] = self.fake_namespace_name
        _kwargs["ratelimit_service"] = self.fake_service_name
        _kwargs["ratelimit_method"] = {"value": "test-fake-method", "type": "NOT_EQUALS", "value_type": "TEXT"}
        _kwargs["ratelimit_arguments"] = [
            {"type": "HEADER", "key": "test-fake-ratelimit-header",
             "value": {"type": "IN", "value": "test-fake-ratelimit-value1,test-fake-ratelimit-value2"}},
            {"type": "METHOD", "key": "$method",
             "value": {"type": "NOT_IN", "value": "POST,DELETE"}},
        ]

        rsp = self.polaris_server.modify_service_ratelimit_rule(**_kwargs)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service_ratelimit_rule = rsp.json()["responses"][0].get("rateLimit", None)
        if return_service_ratelimit_rule is None:
            self.fail("Fail! No return except polaris service ratelimit rule .")
        else:
            re_srv_ratelimit_rule_status = return_service_ratelimit_rule.get("disable", None)
            re_srv_ratelimit_rule_type = return_service_ratelimit_rule.get("type", None)
            re_srv_ratelimit_rule_failover = return_service_ratelimit_rule.get("failover", None)
            re_srv_ratelimit_rule_action = return_service_ratelimit_rule.get("action", None)
            re_srv_ratelimit_rule_max_queue_delay = return_service_ratelimit_rule.get("max_queue_delay", None)
            re_srv_ratelimit_namespace = return_service_ratelimit_rule.get("namespace", None)
            re_srv_ratelimit_service = return_service_ratelimit_rule.get("service", None)
            re_srv_ratelimit_method = return_service_ratelimit_rule.get("method", None)
            re_srv_ratelimit_arguments = return_service_ratelimit_rule.get("arguments", None)

            self.assert_("Fail! No return except polaris service ratelimit rule status.",
                         re_srv_ratelimit_rule_status == _kwargs["disable"])
            self.assert_("Fail! No return except polaris service ratelimit rule type.",
                         re_srv_ratelimit_rule_type == _kwargs["rule_type"])
            self.assert_("Fail! No return except polaris service ratelimit rule failover.",
                         re_srv_ratelimit_rule_failover == _kwargs["failover"])
            self.assert_("Fail! No return except polaris service ratelimit rule action.",
                         re_srv_ratelimit_rule_action == _kwargs["ratelimit_action"])
            self.assert_("Fail! No return except polaris service ratelimit rule max_queue_delay.",
                         re_srv_ratelimit_rule_max_queue_delay == _kwargs["max_queue_delay"])
            self.assert_("Fail! No return except polaris service ratelimit namespace.",
                         re_srv_ratelimit_namespace == _kwargs["ratelimit_namespace"])
            self.assert_("Fail! No return except polaris service ratelimit service.",
                         re_srv_ratelimit_service == _kwargs["ratelimit_service"])
            self.assert_("Fail! No return except polaris service ratelimit method.",
                         re_srv_ratelimit_method == _kwargs["ratelimit_method"])
            self.assert_("Fail! No return except polaris service ratelimit arguments.",
                         len(re_srv_ratelimit_arguments) == len(_kwargs["ratelimit_arguments"]))

        # ===========================
        self.start_step("update rule limit service rule.")
        _kwargs["ratelimit_namespace"] = self.namespace_name
        _kwargs["ratelimit_service"] = self.service_name
        _kwargs["ratelimit_arguments"] = [
            {"type": "HEADER", "key": "test-fake-ratelimit-header",
             "value": {"type": "IN", "value": "test-fake-ratelimit-value1,test-fake-ratelimit-value2"}}
        ]
        _kwargs["ratelimit_amounts"] = [
            {"maxAmount": 1, "validDuration": "1s"},
            {"maxAmount": 10, "validDuration": "60s"}
        ]
        _kwargs["ratelimit_regex_combine"] = False

        rsp = self.polaris_server.modify_service_ratelimit_rule(**_kwargs)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service_ratelimit_rule = rsp.json()["responses"][0].get("rateLimit", None)
        if return_service_ratelimit_rule is None:
            self.fail("Fail! No return except polaris service ratelimit rule .")
        else:
            re_srv_ratelimit_rule_status = return_service_ratelimit_rule.get("disable", None)
            re_srv_ratelimit_rule_type = return_service_ratelimit_rule.get("type", None)
            re_srv_ratelimit_rule_failover = return_service_ratelimit_rule.get("failover", None)
            re_srv_ratelimit_rule_action = return_service_ratelimit_rule.get("action", None)
            re_srv_ratelimit_rule_max_queue_delay = return_service_ratelimit_rule.get("max_queue_delay", None)
            re_srv_ratelimit_namespace = return_service_ratelimit_rule.get("namespace", None)
            re_srv_ratelimit_service = return_service_ratelimit_rule.get("service", None)
            re_srv_ratelimit_method = return_service_ratelimit_rule.get("method", None)
            re_srv_ratelimit_arguments = return_service_ratelimit_rule.get("arguments", None)
            re_srv_ratelimit_amounts = return_service_ratelimit_rule.get("amounts", None)
            re_srv_ratelimit_regex_combine = return_service_ratelimit_rule.get("regex_combine", None)

            self.assert_("Fail! No return except polaris service ratelimit rule status.",
                         re_srv_ratelimit_rule_status == _kwargs["disable"])
            self.assert_("Fail! No return except polaris service ratelimit rule type.",
                         re_srv_ratelimit_rule_type == _kwargs["rule_type"])
            self.assert_("Fail! No return except polaris service ratelimit rule failover.",
                         re_srv_ratelimit_rule_failover == _kwargs["failover"])
            self.assert_("Fail! No return except polaris service ratelimit rule action.",
                         re_srv_ratelimit_rule_action == _kwargs["ratelimit_action"])
            self.assert_("Fail! No return except polaris service ratelimit rule max_queue_delay.",
                         re_srv_ratelimit_rule_max_queue_delay == _kwargs["max_queue_delay"])
            self.assert_("Fail! No return except polaris service ratelimit namespace.",
                         re_srv_ratelimit_namespace == _kwargs["ratelimit_namespace"])
            self.assert_("Fail! No return except polaris service ratelimit service.",
                         re_srv_ratelimit_service == _kwargs["ratelimit_service"])
            self.assert_("Fail! No return except polaris service ratelimit method.",
                         re_srv_ratelimit_method == _kwargs["ratelimit_method"])
            self.assert_("Fail! No return except polaris service ratelimit arguments.",
                         len(re_srv_ratelimit_arguments) == len(_kwargs["ratelimit_arguments"]))
            self.assert_("Fail! No return except polaris service ratelimit amounts.",
                         len(re_srv_ratelimit_amounts) == len(_kwargs["ratelimit_amounts"]))
            self.assert_("Fail! No return except polaris service ratelimit regex combine.",
                         re_srv_ratelimit_regex_combine == _kwargs["ratelimit_regex_combine"])

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, namespace_names=[self.namespace_name, self.fake_namespace_name])


if __name__ == '__main__':
    ServiceRatelimitModifyCheck().debug_run()
