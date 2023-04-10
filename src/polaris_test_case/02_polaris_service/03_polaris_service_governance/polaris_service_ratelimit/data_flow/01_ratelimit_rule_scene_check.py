import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class RatelimitScene01Check(PolarisTestCase):
    """
    Used to check ratelimit dataflow scene 01.

    Ratelimit type: Standalone ratelimit
    Target Service(Interface): default:RateLimitCalleeService:*
    Request traffic portrait: Custom-Label test-key1 EQUAL test-value1
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
        self.ratelimit_rule_name = "RatelimitSceneCheck-" + _random_str

        # ===========================
        self.start_step("Create local service ratelimit rule %s to limit service %s in %s." % (
            self.ratelimit_rule_name, ratelimit_callee_service, ratelimit_callee_namespace))

        self.create_service_ratelimit_rule_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_RATELIMIT_PATH

        srv_ratelimit_rule_failover = "FAILOVER_LOCAL"
        srv_ratelimit_rule_type = "LOCAL"
        metadata_key = "test-key-1"
        metadata_value = "test-value-1"
        rsp = self.polaris_server.create_service_ratelimit_rule(
            self.create_service_ratelimit_rule_url, self.ratelimit_rule_name, rule_type=srv_ratelimit_rule_type,
            ratelimit_namespace=ratelimit_callee_namespace, ratelimit_service=ratelimit_callee_service,
            ratelimit_method={"value": "", "type": "EXACT"},
            ratelimit_arguments=[{"type": "CUSTOM",
                                  "key": metadata_key,
                                  "value": {"type": "EXACT", "value": metadata_value}}],
            ratelimit_amounts=[{"maxAmount": 5, "validDuration": "10s"}],
            ratelimit_regex_combine=True, ratelimit_action="REJECT", failover=srv_ratelimit_rule_failover,
            disable=False)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        # ===========================
        self.start_step("Wait 10s to request sct consumer to check provider ratelimit.")
        time.sleep(10)
        cmd_curl = "curl -sv 'http://127.0.0.1:%s/business/invoke'" % ratelimit_caller_port
        rsp, stderr = self.execute_shell(cmd_curl, timeout=15)
        # business/invoke will invoke ratelimit callee 30 times,
        # and the 2 callee instances will be limited for at least 19 times
        self.assert_("Fail! No return except rate limit times.", rsp.count("TooManyRequests") >= 19)
        # ===========================
        self.start_step("Wait 15s to request sct consumer to check provider ratelimit.")
        time.sleep(15)
        cmd_curl = "curl -sv 'http://127.0.0.1:%s/business/invoke'" % ratelimit_caller_port
        rsp, stderr = self.execute_shell(cmd_curl, timeout=15)
        # business/invoke will invoke ratelimit callee 30 times,
        # and the 2 callee instances will be limited for at least 19 times
        self.assert_("Fail! No return except rate limit times.", rsp.count("TooManyRequests") <= 21)


if __name__ == '__main__':
    RatelimitScene01Check().debug_run()
