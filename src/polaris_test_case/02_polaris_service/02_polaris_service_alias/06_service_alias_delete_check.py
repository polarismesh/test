import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateServiceRequest, DeleteServiceRequest, DeleteServiceAliasRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceAliasDeleteCheck(PolarisTestCase):
    """
    Used to test delete service alias.

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
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.namespace_name = "AutoTestPolarisServiceAliasNamespace-" + _random_str
        self.alias_namespace_name = "AutoTestPolarisServiceAliasNamespace2-" + _random_str
        self.service_name = "AutoTestPolarisServiceAliasService-" + _random_str
        self.service_name2 = "AutoTestPolarisServiceAliasService2-" + _random_str
        self.service_alias_name = "AutoTestPolarisServiceAlias-" + _random_str
        self.service_alias_name2 = "AutoTestPolarisServiceAlias2-" + _random_str

        self.create_single_namespace(self.polaris_server, namespace_name=self.namespace_name)
        self.create_single_namespace(self.polaris_server, namespace_name=self.alias_namespace_name)
        self.create_single_service(self.polaris_server, self.service_name, self.namespace_name)
        self.create_single_service(self.polaris_server, self.service_name2, self.namespace_name)
        # ===========================
        # alias-1
        self.create_single_service_alias(polaris_server=self.polaris_server, service_name=self.service_name,
                                         namespace_name=self.namespace_name, service_alias_name=self.service_alias_name,
                                         alias_namespace_name=self.alias_namespace_name)
        # alias-2
        self.create_single_service_alias(polaris_server=self.polaris_server, service_name=self.service_name2,
                                         namespace_name=self.namespace_name,
                                         service_alias_name=self.service_alias_name2,
                                         alias_namespace_name=self.alias_namespace_name)

        # ===========================
        self.start_step("Delete error polaris service.")
        delete_srv_alias_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.DELETE_SERVICE_ALIAS_PATH
        err_srv_alias_name = self.service_alias_name + "-err"
        delete_srv_alias_req = DeleteServiceAliasRequest(alias_namespace_name=self.alias_namespace_name,
                                                         alias_name=err_srv_alias_name)

        rsp = self.polaris_server.delete_service_alias(delete_srv_alias_url, delete_srv_alias_req)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 400304)
        # ===========================
        self.start_step("Delete correct polaris service aliases.")
        delete_srv_alias_reqs = [
            DeleteServiceAliasRequest(alias_namespace_name=self.alias_namespace_name,
                                      alias_name=self.service_alias_name),
            DeleteServiceAliasRequest(alias_namespace_name=self.alias_namespace_name,
                                      alias_name=self.service_alias_name2),
        ]
        rsp = self.polaris_server.delete_service_alias(delete_srv_alias_url, delete_srv_alias_reqs)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Describe all service aliases to check delete result.")
        return_service_aliases = self.get_all_service_aliases(self.polaris_server)
        return_service_aliases_names = [alias["alias"] for alias in return_service_aliases]

        self.assert_("Fail! Deleted polaris service alias still exist.",
                     self.service_alias_name not in return_service_aliases_names)
        self.assert_("Fail! Deleted polaris service alias still exist.",
                     self.service_alias_name2 not in return_service_aliases_names)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name])
        self.clean_test_namespaces(self.polaris_server, [self.alias_namespace_name])


if __name__ == '__main__':
    ServiceAliasDeleteCheck().debug_run()
