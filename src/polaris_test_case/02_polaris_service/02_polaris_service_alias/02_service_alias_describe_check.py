import random
import string

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceAliasDescribeCheck(PolarisTestCase):
    """
    Used to test describe service alias.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def check_return_service_alias(self, check_total, check_size, check_polaris_code, check_srv_alias_names, **kwargs):
        rsp = self.polaris_server.describe_service_alias(**kwargs)

        polaris_code = rsp.json().get("code", None)
        return_service_aliases_total = rsp.json().get("amount", None)
        return_service_aliases_size = rsp.json().get("size", None)

        self.assert_("Fail! No return except polaris code.", polaris_code == check_polaris_code)
        if check_total != -1:
            self.assert_("Fail! No return except polaris amount.", return_service_aliases_total == check_total)
        self.assert_("Fail! No return except polaris service aliases size.", return_service_aliases_size == check_size)

        return_srv_aliases = rsp.json().get("aliases", None)
        srv_alias_names = [alias["alias"] for alias in return_srv_aliases]
        self.assert_("Fail! No return except polaris service aliases.",
                     srv_alias_names.sort() == check_srv_alias_names.sort())

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        # ===========================
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.namespace_name = "AutoTestPolarisServiceAliasNamespace-" + _random_str
        self.alias_namespace_name = "AutoTestPolarisServiceAliasNamespace2-" + _random_str
        self.alias_namespace_name2 = "AutoTestPolarisServiceAliasNamespace3-" + _random_str
        self.service_name = "AutoTestPolarisServiceAliasService-" + _random_str
        self.service_name2 = "AutoTestPolarisServiceAliasService2-" + _random_str
        self.service_alias_name = "AutoTestPolarisServiceAlias-" + _random_str
        self.service_alias_name2 = "AutoTestPolarisServiceAlias2-" + _random_str
        self.service_alias_name3 = "AutoTestPolarisServiceAlias3-" + _random_str
        self.service_alias_name4 = "AutoTestPolarisServiceAlias4-" + _random_str

        self.create_single_namespace(self.polaris_server, namespace_name=self.namespace_name)
        self.create_single_namespace(self.polaris_server, namespace_name=self.alias_namespace_name)
        self.create_single_namespace(self.polaris_server, namespace_name=self.alias_namespace_name2)
        self.create_single_service(self.polaris_server, self.service_name, self.namespace_name)
        self.create_single_service(self.polaris_server, self.service_name2, self.namespace_name)
        # ===========================
        # alias-1
        self.create_single_service_alias(polaris_server=self.polaris_server, service_name=self.service_name,
                                         namespace_name=self.namespace_name, service_alias_name=self.service_alias_name,
                                         alias_namespace_name=self.alias_namespace_name)
        # alias-2, alias-1,2 同命名空间同指向服务
        self.create_single_service_alias(polaris_server=self.polaris_server, service_name=self.service_name,
                                         namespace_name=self.namespace_name,
                                         service_alias_name=self.service_alias_name2,
                                         alias_namespace_name=self.alias_namespace_name)
        # alias-3, alias-2,3 同命名空间不同指向服务
        self.create_single_service_alias(polaris_server=self.polaris_server, service_name=self.service_name2,
                                         namespace_name=self.namespace_name,
                                         service_alias_name=self.service_alias_name3,
                                         alias_namespace_name=self.alias_namespace_name)
        # alias-4, alias-1,4 不同命名空间同指向服务
        self.create_single_service_alias(polaris_server=self.polaris_server, service_name=self.service_name2,
                                         namespace_name=self.namespace_name,
                                         service_alias_name=self.service_alias_name4,
                                         alias_namespace_name=self.alias_namespace_name2)

        # ===========================
        self.start_step("Check describe all service aliases.")
        return_service_aliases = self.get_all_service_aliases(self.polaris_server)

        return_service_aliases_names = [alias["alias"] for alias in return_service_aliases]
        _check_aliases = [self.service_alias_name, self.service_alias_name2, self.service_alias_name3,
                          self.service_alias_name4]
        if return_service_aliases_names:
            for re_service_aliases_name in return_service_aliases_names:
                self.log_info("service aliases %s wait for check." % _check_aliases)
                if _check_aliases:
                    if re_service_aliases_name in _check_aliases:
                        self.log_info("Success to check return service aliases %s!" % re_service_aliases_name)
                        _check_aliases.remove(re_service_aliases_name)
                    else:
                        self.log_info("No return except polaris service aliases %s." % re_service_aliases_name)
                else:
                    self.log_info("Success to check all service aliases!")
                    break
        else:
            self.fail("Fail! No return except polaris service aliases.")

        # ===========================
        self.start_step("Check describe service aliases by correct alias namespace name.")
        _kwargs = {"url": self.describe_service_alias_url, "alias_namespace_name": self.alias_namespace_name,
                   "limit": 10, "offset": 0}
        self.check_return_service_alias(
            check_total=3, check_size=3, check_polaris_code=200000,
            check_srv_alias_names=[self.service_alias_name, self.service_alias_name2, self.service_alias_name3],
            **_kwargs)

        # ===========================
        self.start_step("Check describe service aliases by error alias namespace name.")
        _kwargs = {"url": self.describe_service_alias_url, "alias_namespace_name": self.alias_namespace_name + "err",
                   "limit": 10, "offset": 0}
        self.check_return_service_alias(check_total=0, check_size=0, check_polaris_code=200000,
                                        check_srv_alias_names=[], **_kwargs)

        # ===========================
        self.start_step("Check describe service aliases by correct alias point to service name.")
        _kwargs = {"url": self.describe_service_alias_url, "point_to_service_name": self.service_name,
                   "limit": 10, "offset": 0}
        self.check_return_service_alias(
            check_total=2, check_size=2, check_polaris_code=200000,
            check_srv_alias_names=[self.service_alias_name, self.service_alias_name2], **_kwargs)

        # ===========================
        self.start_step("Check describe service aliases by error alias point to service name.")
        _kwargs = {"url": self.describe_service_alias_url, "point_to_service_name": self.service_name + "err",
                   "limit": 10, "offset": 0}
        self.check_return_service_alias(check_total=0, check_size=0, check_polaris_code=200000,
                                        check_srv_alias_names=[], **_kwargs)

        # ===========================
        self.start_step(
            "Check describe service aliases by correct alias namespace name and correct alias point to service name.")
        _kwargs = {"url": self.describe_service_alias_url, "alias_namespace_name": self.alias_namespace_name,
                   "point_to_service_name": self.service_name, "limit": 10, "offset": 0}
        self.check_return_service_alias(
            check_total=2, check_size=2, check_polaris_code=200000,
            check_srv_alias_names=[self.service_alias_name, self.service_alias_name2],
            **_kwargs)

        # ===========================
        self.start_step("Check describe service aliases limit and offset.")
        _kwargs = {"url": self.describe_service_alias_url, "limit": 10, "offset": 100}
        self.check_return_service_alias(check_total=-1, check_size=0, check_polaris_code=200000,
                                        check_srv_alias_names=[], **_kwargs)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name])
        self.clean_test_namespaces(self.polaris_server, [self.alias_namespace_name])
        self.clean_test_namespaces(self.polaris_server, [self.alias_namespace_name2])


if __name__ == '__main__':
    ServiceAliasDescribeCheck().debug_run()
