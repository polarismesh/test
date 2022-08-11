import os
import time

from testbase import TestCase
from testbase.conf import settings

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateNamespaceRequest, DeleteNamespaceRequest


class PolarisTestCase(TestCase):
    # Specify the configuration file location.
    os.environ["QTAF_SETTINGS_MODULE"] = "src.settings"

    def pre_test(self):
        # ===========================
        self.start_step("Get POLARIS_CONSOLE_ADDR configuration.")
        POLARIS_CONSOLE_ADDR = settings.get("POLARIS_CONSOLE_ADDR", None)
        if POLARIS_CONSOLE_ADDR is not None:
            self.log_info("POLARIS_CONSOLE_ADDR: %s" % POLARIS_CONSOLE_ADDR)
            self.polaris_console_addr = POLARIS_CONSOLE_ADDR
        else:
            self.fail("Check your config file in [{config_dir}] and set POLARIS_CONSOLE_ADDR in [{config_dir}]."
                      .format(config_dir=os.environ["QTAF_SETTINGS_MODULE"]))

    def run_test(self):
        pass

    def get_console_token(self, username="polaris", password="polaris"):
        # ===========================
        self.start_step("Get polaris main user console token.")
        login_url = "http://" + self.polaris_console_addr + PolarisServer.LOGIN_PATH
        rsp = PolarisServer.get_initial_token(url=login_url, username=username, password=password)
        self.token = rsp.json().get("loginResponse", None).get("token", None)
        self.user_id = rsp.json().get("loginResponse", None).get("user_id", None)

    def create_single_namespace(self, polaris_server, namespace_name=None):
        # ===========================
        self.start_step("Create one regular polaris namespace.")
        self.create_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.NAMESPACE_PATH
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        self.create_namespace_request = CreateNamespaceRequest(namespace_name=namespace_name,
                                                               comment="Auto test create polaris namespace %s" % now)
        rsp = polaris_server.create_namespace(self.create_namespace_url, self.create_namespace_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_namespace = rsp.json()["responses"][0].get("namespace", None)
        if return_namespace is None:
            self.fail("Fail! No return except polaris namespace.")
            return
        else:
            re_namespace_name = return_namespace.get("name", None)
            self.assert_("Fail! No return except polaris namespace name.", re_namespace_name == namespace_name)

        if self.test_result.passed:
            self.log_info("Success to check return namespace and polaris code!")

    def clean_test_namespaces(self, polaris_server, namespace_name):
        # ===========================
        self.start_step("Test case finished, clean the test polaris namespaces.")
        delete_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_NAMESPACE_PATH

        delete_namespace_requests = []
        for n in namespace_name:
            delete_namespace_requests.append(DeleteNamespaceRequest(namespace_name=n))
        rsp = polaris_server.delete_namespace(delete_namespace_url, delete_namespace_requests)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

    def get_all_namespaces(self, polaris_server, limit=10):
        self.describe_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.NAMESPACE_PATH
        rsp = polaris_server.describe_namespace(self.describe_namespace_url, limit=limit, offset=0)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_namespace_total = rsp.json().get("amount", None)

        return_namespaces = []
        if return_namespace_total > limit:
            self.log_info("requery with the total number of Polaris namespaces.")
            query_times = (return_namespace_total / limit) + 1
            for offset in range(query_times):
                rsp = polaris_server.describe_namespace(self.describe_namespace_url,
                                                        limit=return_namespace_total, offset=offset)
                polaris_code = rsp.json().get("code", None)
                self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

                return_namespaces += rsp.json().get("namespaces", None)
        else:
            return_namespaces = rsp.json().get("namespaces", None)
        return return_namespaces