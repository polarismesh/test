import random
import string
import subprocess

from testbase.conf import settings
from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class NamespaceCreateFromGRPCApiCheck(PolarisTestCase):
    """
    Used to test creating namespace from grpc.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.start_step("Create one polaris namespace from grpc demo.")
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.namespace_name = "AutoTestPolarisGRPCNamespace-" + _random_str
        self.service_name = "AutoTestPolarisGRPCService-" + _random_str

        # ===========================
        new_directory = self.create_temp_test_directory(temp_dir_suffix=_random_str, resource_name="polaris-go-demo")

        # ===========================
        self.start_step(
            "Register by grpc demo[https://github.com/polarismesh/polaris-go/tree/main/examples/quickstart/provider], "
            "auto create namespace if not exist.")
        self.log_info("The polaris-server.yaml default config: namespace.autoCreate=true has been pre-set, "
                      "if this case fail, please check your polaris-server.yaml.")
        reg_ip = settings.POLARIS_SERVER_GRPC_SERVICE_ADDR
        cmd_exe = "cd %s && chmod 777 provider && sed -i 's/ipaddr/%s/g' polaris.yaml && " \
                  "nohup ./provider -service=%s -namespace=%s -auto_shutdown=true &" % \
                  (new_directory, reg_ip, self.service_name, self.namespace_name)
        self.execute_shell(cmd_exe, timeout=30)

        # ===========================
        self.start_step("Check create namespace.")
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        return_namespaces = self.get_all_namespaces(self.polaris_server)
        return_namespace_names = [ns["name"] for ns in return_namespaces]
        self.assert_("Fail! No return except polaris namespace.", self.namespace_name in return_namespace_names)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name])


if __name__ == '__main__':
    NamespaceCreateFromGRPCApiCheck().debug_run()
