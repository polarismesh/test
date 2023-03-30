import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import ModifyNamespaceRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class NamespaceModifyCheck(PolarisTestCase):
    """
    Used to test describe namespace.

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
        time.sleep(2)
        self.start_step("Modify this polaris namespace comment.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test update polaris namespace %s" % now
        self.modify_namespace_url = self.create_namespace_url

        modify_namespace_request = ModifyNamespaceRequest(namespace_name=self.namespace_name, comment=comment)
        rsp = self.polaris_server.modify_namespace(self.modify_namespace_url, modify_namespace_request)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_namespace = rsp.json()["responses"][0].get("namespace", None)
        if return_namespace is None:
            self.fail("Fail! No return except polaris namespace.")
            return
        else:
            re_namespace_name = return_namespace.get("name", None)
            self.assert_("Fail! No return except polaris namespace name.", re_namespace_name == self.namespace_name)
            re_namespace_comment = return_namespace.get("comment", None)
            self.assert_("Fail! No return except polaris namespace comment.", re_namespace_comment == comment)

        if self.test_result.passed:
            self.log_info("Success to check return namespace and polaris code!")

        # ===========================
        self.start_step("Create another regular polaris namespace.")
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.namespace_name2 = "AutoTestPolarisNamespace-" + _random_str
        self.create_single_namespace(self.polaris_server, self.namespace_name2)

        # ===========================
        time.sleep(2)
        self.start_step("Bath Modify these polaris namespaces comment.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test update polaris namespace %s" % now

        modify_namespace_requests = [
            ModifyNamespaceRequest(namespace_name=self.namespace_name, comment=comment),
            ModifyNamespaceRequest(namespace_name=self.namespace_name2, comment=comment)
        ]
        rsp = self.polaris_server.modify_namespace(self.modify_namespace_url, modify_namespace_requests)
        for res in rsp.json()["responses"]:
            return_namespace = res.get("namespace", None)
            if return_namespace is None:
                self.fail("Fail! No return except polaris namespace.")
                return
            else:
                re_namespace_name = return_namespace.get("name", None)
                self.log_info("check namespace %s updated comment." % re_namespace_name)
                re_namespace_comment = return_namespace.get("comment", None)
                self.assert_("Fail! No return except polaris namespace comment.", re_namespace_comment == comment)
                if self.test_result.passed:
                    self.log_info("Success to check return namespace %s!" % re_namespace_name)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name, self.namespace_name2])


if __name__ == '__main__':
    NamespaceModifyCheck().debug_run()
