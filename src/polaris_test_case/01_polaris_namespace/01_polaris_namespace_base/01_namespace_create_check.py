import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateNamespaceRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class NamespaceCreateCheck(PolarisTestCase):
    """
    Used to test creating namespace.

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
        self.namespace_name = "AutoTestPolarisNamespace"
        self.create_single_namespace(self.polaris_server, self.namespace_name)
        # ===========================
        self.start_step("Bath Create two regular polaris namespace.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test create polaris namespace %s" % now
        self.namespace_name2 = "AutoTestPolarisNamespace2"
        self.namespace_name3 = "AutoTestPolarisNamespace3"
        create_namespace_request_list = []

        batch_create_namespace_names = [self.namespace_name2, self.namespace_name3]
        for n in batch_create_namespace_names:
            create_namespace_request_list.append(CreateNamespaceRequest(namespace_name=n, comment=comment))

        rsp = self.polaris_server.create_namespace(self.create_namespace_url, create_namespace_request_list)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        _check_ns_names = batch_create_namespace_names.copy()
        for res in rsp.json()["responses"]:
            self.log_info("namespace %s wait for check." % _check_ns_names)
            return_namespace = res.get("namespace", None)
            if return_namespace is None:
                self.fail("Fail! No return except polaris namespace.")
                return
            else:
                re_namespace_name = return_namespace.get("name", None)
                self.assert_("Fail! No return except polaris namespace name.", re_namespace_name in _check_ns_names)
                if self.test_result.passed:
                    self.log_info("Success to check return namespace %s!" % re_namespace_name)
                    _check_ns_names.remove(re_namespace_name)

        # ===========================
        self.start_step("Create one repeat polaris namespace.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        self.create_namespace_request.comment = "Auto test create polaris namespace %s" % now
        rsp = self.polaris_server.create_namespace(self.create_namespace_url, self.create_namespace_request)
        polaris_code = rsp.json().get("code", None)
        re_polaris_info = rsp.json()["responses"][0].get("info", None)
        re_polaris_code = rsp.json()["responses"][0].get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code != 200000)
        self.assert_("Fail! No return except polaris code.", re_polaris_code == 400201)
        self.assert_("Fail! No return except polaris info.", "existed resource" in re_polaris_info)
        if self.test_result.passed:
            self.log_info("Success to check return token and polaris code!")

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server,
                                   [self.namespace_name, self.namespace_name2, self.namespace_name3])


if __name__ == '__main__':
    NamespaceCreateCheck().debug_run()
