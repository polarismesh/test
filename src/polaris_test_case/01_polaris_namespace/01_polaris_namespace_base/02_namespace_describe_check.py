import random
import string

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class NamespaceDescribeCheck(PolarisTestCase):
    """
    Used to test describe namespace.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def check_return_ns(self, check_total, check_size, check_polaris_code, check_namespace_names, **kwargs):
        rsp = self.polaris_server.describe_namespace(**kwargs)
        polaris_code = rsp.json().get("code", None)
        return_namespace_total = rsp.json().get("amount", None)
        return_namespace_size = rsp.json().get("size", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == check_polaris_code)
        if check_total != -1:
            self.assert_("Fail! No return except polaris amount.", return_namespace_total == check_total)
        self.assert_("Fail! No return except polaris namespaces size.", return_namespace_size == check_size)

        return_namespaces = rsp.json().get("namespaces", None)
        return_namespace_names = [ns["name"] for ns in return_namespaces]
        self.assert_("Fail! No return except polaris namespace.",
                     return_namespace_names.sort() == check_namespace_names.sort())

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
        self.start_step("Default describe namespaces.")
        return_namespaces = self.get_all_namespaces(self.polaris_server)
        return_namespace_names = [ns["name"] for ns in return_namespaces]
        _check_ns_names = ["Polaris", "default", self.namespace_name]
        if return_namespace_names:
            for re_namespace_name in return_namespace_names:
                self.log_info("namespace %s wait for check." % _check_ns_names)
                if _check_ns_names:
                    if re_namespace_name in _check_ns_names:
                        self.log_info("Success to check return namespace %s!" % re_namespace_name)
                        _check_ns_names.remove(re_namespace_name)
                    else:
                        self.log_info("No return except polaris namespace %s." % re_namespace_name)
                else:
                    self.log_info("Success to check all namespaces!")
                    break
        else:
            self.fail("Fail! No return except polaris namespaces.")
        # ===========================
        self.start_step("Check describe namespaces by correct namespace name.")
        _kwargs = {"url": self.describe_namespace_url, "namespace_name": self.namespace_name, "limit": 10, "offset": 0}
        self.check_return_ns(check_total=1, check_size=1, check_polaris_code=200000,
                             check_namespace_names=[self.namespace_name], **_kwargs)

        # ===========================
        self.start_step("Check describe namespaces by error namespace name.")
        _kwargs = {"url": self.describe_namespace_url, "namespace_name": self.namespace_name + "err",
                   "limit": 10, "offset": 0}
        self.check_return_ns(check_total=0, check_size=0, check_polaris_code=200000,
                             check_namespace_names=[], **_kwargs)

        # ===========================
        self.start_step("Check describe namespaces limit and offset.")
        _kwargs = {"url": self.describe_namespace_url, "limit": 10, "offset": 100}
        self.check_return_ns(check_total=-1, check_size=0, check_polaris_code=200000,
                             check_namespace_names=[], **_kwargs)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name])


if __name__ == '__main__':
    NamespaceDescribeCheck().debug_run()
