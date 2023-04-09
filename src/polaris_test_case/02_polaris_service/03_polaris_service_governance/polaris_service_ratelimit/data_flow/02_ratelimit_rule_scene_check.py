import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class RatelimitScene02Check(PolarisTestCase):
    """
    Used to check ratelimit dataflow scene 02.

    Ratelimit type: Standalone ratelimit
    Target Service(Interface): default:RateLimitCalleeService:EXACT /business/info
    Request traffic portrait: HEADER test-header-key1 IN test-header-value1,test-header-value2
    Ratelimit conditions: Second-Level 5 times in 10 seconds
    Ratelimit Scheme: Fail Fast

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        cmd_get_caller_port = "ps axu| grep Kona| grep ratelimit-caller| grep -v 'sh -c'| awk '{print $17}'|awk -F'=' '{print $2}'"
        ratelimit_caller_port, stderr = self.execute_shell(cmd_get_caller_port, timeout=10)
        ratelimit_caller_port = ratelimit_caller_port.replace("\n", "")
        ratelimit_callee_namespace = "default"
        ratelimit_callee_service = "RateLimitCalleeService"

        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.ratelimit_rule_name = "RatelimitSceneCheck-"

        self.service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_RATELIMIT_PATH
        _kwargs = {"url": self.service_ratelimit_rule_url, "ratelimit_rule_name": self.ratelimit_rule_name,
                   "limit": 10, "offset": 0}
        rsp = self.polaris_server.describe_service_ratelimit_rule(**_kwargs)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        rule_id = rsp.json().get("rateLimits", None)[0]["id"]

        # ===========================
        self.start_step("Modify local service ratelimit rule.")

        srv_ratelimit_rule_failover = "FAILOVER_LOCAL"
        srv_ratelimit_rule_type = "LOCAL"
        header_key = "test-header-key-1"
        header_value = "test-header-value-1,test-header-value-2"
        rsp = self.polaris_server.modify_service_ratelimit_rule(
            self.service_ratelimit_rule_url, rule_id, rule_type=srv_ratelimit_rule_type,
            ratelimit_namespace=ratelimit_callee_namespace, ratelimit_service=ratelimit_callee_service,
            ratelimit_method={"value": "/business/info", "type": "EXACT"},
            ratelimit_arguments=[{"type": "HEADER",
                                  "key": header_key,
                                  "value": {"type": "IN", "value": header_value}}],
            ratelimit_amounts=[{"maxAmount": 5, "validDuration": "10s"}],
            ratelimit_regex_combine=True, ratelimit_action="REJECT", failover=srv_ratelimit_rule_failover,
            disable=False)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        # ===========================
        self.start_step(
            "Wait 10s to request sct consumer to check provider ratelimit: test-header-key1:test-header-value1 will be limited.")
        time.sleep(10)
        cmd_curl = "curl -sv -H'test-header-key1:test-header-value1' 'http://127.0.0.1:%s/business/invoke'" % ratelimit_caller_port
        rsp, stderr = self.execute_shell(cmd_curl, timeout=15)
        # business/invoke will invoke ratelimit callee 30 times,
        # and the 2 callee instances will be limited for at least 19 times
        self.assert_("Fail! No return except rate limit times.", rsp.count("TooManyRequests") >= 19)
        # ===========================
        self.start_step(
            "Request sct consumer to check provider ratelimit: test-header-key1:test-header-value2 will be limited.")
        cmd_curl = "curl -sv -H'test-header-key1:test-header-value2' 'http://127.0.0.1:%s/business/invoke'" % ratelimit_caller_port
        rsp, stderr = self.execute_shell(cmd_curl, timeout=15)
        # business/invoke will invoke ratelimit callee 30 times,
        # and the 2 callee instances will be limited for at least 19 times
        self.assert_("Fail! No return except rate limit times.", rsp.count("TooManyRequests") >= 19)
        # ===========================
        self.start_step(
            "Request sct consumer to check provider ratelimit: test-header-key1:test-header-value3 will not be limited.")
        cmd_curl = "curl -sv -H'test-header-key1:test-header-value3' 'http://127.0.0.1:%s/business/invoke'" % ratelimit_caller_port
        rsp, stderr = self.execute_shell(cmd_curl, timeout=15)
        self.assert_("Fail! No return except rate limit times.", rsp.count("TooManyRequests") <= 0)
        # ===========================
        self.start_step(
            "Request sct consumer to check provider ratelimit: test-header-key2:test-header-value1 will not be limited.")
        cmd_curl = "curl -sv -H'test-header-key2:test-header-value1' 'http://127.0.0.1:%s/business/invoke'" % ratelimit_caller_port
        rsp, stderr = self.execute_shell(cmd_curl, timeout=15)
        self.assert_("Fail! No return except rate limit times.", rsp.count("TooManyRequests") <= 0)


if __name__ == '__main__':
    RatelimitScene02Check().debug_run()
