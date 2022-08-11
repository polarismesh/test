import os
import socket
import string
import subprocess
import time
import random

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
        self.service_name = "AutoTestPolarisGRPCService--" + _random_str

        # ===========================
        test_now_dir = os.path.abspath(__file__)
        self.log_info("Polaris-test now directory: " + test_now_dir)
        test_root_dir = os.path.abspath(os.path.join(os.getcwd(), "../../../.."))
        self.log_info("Polaris-test root directory: " + test_root_dir)
        test_resource_dir = test_root_dir + "/polaris_test_resource/polaris-go-demo"
        self.log_info("Polaris-test resource directory: " + test_resource_dir)

        case_name = type(self).__name__.lower()
        new_directory = "%s/temp-test/%s-%s" % (test_root_dir, case_name, _random_str)
        cmd_pre_deal_1 = "mkdir -p %s" % new_directory
        if os.system(cmd_pre_deal_1) != 0:
            raise RuntimeError("Exec cmd %s error!" % cmd_pre_deal_1)

        cmd_pre_deal_2 = "cp -r %s/* /root/%s" % (test_resource_dir, new_directory)
        if os.system(cmd_pre_deal_2) != 0:
            raise RuntimeError("Exec cmd %s error!" % cmd_pre_deal_2)

        reg_ip = settings.POLARIS_SERVER_GRPC_SERVICE_ADDR
        host = socket.gethostbyname(socket.gethostname())
        port = random.randint(30000, 50000)
        cmd_exe = "cd /root/%s && chmod 777 provider && sed -i 's/ipaddr/%s:8091/g' polaris.yaml && " \
                  "nohup ./provider --service=%s --namespace=%s --host=%s --port=%s &" % \
                  (new_directory, reg_ip, self.service_name, self.namespace_name, host, port)
        rsp = subprocess.call(cmd_exe, shell=True)
        self.log_info(rsp)

    # def post_test(self):
    #     self.clean_test_services()
    #     self.clean_test_namespaces(self.polaris_server,
    #                                [self.namespace_name, self.namespace_name2, self.namespace_name3])


if __name__ == '__main__':
    NamespaceCreateFromGRPCApiCheck().debug_run()
