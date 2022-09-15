import random
import string
from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import DeleteNamespaceRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class NamespaceDeleteCheck(PolarisTestCase):
    """
    Used to test delete namespace.

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
        self.start_step("Create one regular polaris namespace.")
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.namespace_name = "AutoTestPolarisNamespace-" + _random_str
        self.create_single_namespace(self.polaris_server, self.namespace_name)
        # ===========================
        self.start_step("Delete error polaris namespace.")
        delete_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_NAMESPACE_PATH
        delete_namespace_request = DeleteNamespaceRequest(namespace_name="AutoTestPolarisNamespace-delete-error")
        rsp = self.polaris_server.delete_namespace(delete_namespace_url, delete_namespace_request)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Delete correct polaris namespace.")
        delete_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_NAMESPACE_PATH
        delete_namespace_request = DeleteNamespaceRequest(namespace_name=self.namespace_name)
        rsp = self.polaris_server.delete_namespace(delete_namespace_url, delete_namespace_request)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Describe all namespaces to check delete result.")
        self.describe_namespace_url = self.create_namespace_url
        limit = 10
        rsp = self.polaris_server.describe_namespace(self.describe_namespace_url, limit=limit, offset=0)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_namespace_total = rsp.json().get("amount", None)

        return_namespaces = []
        if return_namespace_total > limit:
            self.log_info("requery with the total number of Polaris namespaces.")
            query_times = (return_namespace_total / limit) + 1
            for offset in range(query_times):
                rsp = self.polaris_server.describe_namespace(self.describe_namespace_url, limit=limit, offset=offset)
                polaris_code = rsp.json().get("code", None)
                self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

                return_namespaces += rsp.json().get("namespaces", None)
        else:
            return_namespaces = rsp.json().get("namespaces", None)

        return_namespace_names = [ns["name"] for ns in return_namespaces]
        self.assert_("Fail! Deleted polaris namespace still exist.", self.namespace_name not in return_namespace_names)


if __name__ == '__main__':
    NamespaceDeleteCheck().debug_run()
