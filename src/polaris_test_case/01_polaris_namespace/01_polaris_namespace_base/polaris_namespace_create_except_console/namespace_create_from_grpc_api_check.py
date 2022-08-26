import os
import random
import socket
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
        self.start_step("Get directory.")
        test_now_dir = os.path.abspath(__file__)
        self.log_info("Polaris-test now directory: " + test_now_dir)
        test_root_dir = os.path.abspath(os.path.join(test_now_dir, "../../../../.."))
        self.log_info("Polaris-test root directory: " + test_root_dir)
        test_resource_dir = test_root_dir + "/polaris_test_resource/polaris-go-demo"
        self.log_info("Polaris-test resource directory: " + test_resource_dir)

        # ===========================
        self.start_step("Create temp test directory.")
        case_name = type(self).__name__.lower()
        new_directory = "%s/temp-test/%s-%s" % (test_root_dir, case_name, _random_str)
        cmd_pre_deal_1 = "mkdir -p %s" % new_directory
        if os.system(cmd_pre_deal_1) != 0:
            raise RuntimeError("Exec cmd: %s error!" % cmd_pre_deal_1)
        else:
            self.log_info("Exec cmd: %s success!" % cmd_pre_deal_1)

        cmd_pre_deal_2 = "cp -r %s/* %s/" % (test_resource_dir, new_directory)
        if os.system(cmd_pre_deal_2) != 0:
            raise RuntimeError("Exec cmd: %s error!" % cmd_pre_deal_2)
        else:
            self.log_info("Exec cmd: %s success!" % cmd_pre_deal_2)

        # ===========================
        self.start_step("Register by grpc demo, auto create namespace if not exist.")
        self.log_info("The polaris-server.yaml default config: namespace.autoCreate=true has been pre-set, "
                      "if this case fail, please check your polaris-server.yaml.")
        reg_ip = settings.POLARIS_SERVER_GRPC_SERVICE_ADDR
        cmd_exe = "cd %s && chmod 777 provider && sed -i 's/ipaddr/%s/g' polaris.yaml && " \
                  "nohup ./provider -service=%s -namespace=%s -auto_shutdown=true &" % \
                  (new_directory, reg_ip, self.service_name, self.namespace_name)
        self.log_info("Exec cmd: %s" % cmd_exe)
        rsp = subprocess.check_output(cmd_exe, shell=True)
        self.log_info("\n" + rsp.decode())

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
