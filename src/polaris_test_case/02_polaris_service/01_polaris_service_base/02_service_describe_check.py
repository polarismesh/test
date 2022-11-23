import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateServiceRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceDescribeCheck(PolarisTestCase):
    """
    Used to test describe service.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def check_return_service(self, check_total, check_size, check_polaris_code, check_service_names, **kwargs):
        rsp = self.polaris_server.describe_service(**kwargs)

        polaris_code = rsp.json().get("code", None)
        return_service_total = rsp.json().get("amount", None)
        return_service_size = rsp.json().get("size", None)

        self.assert_("Fail! No return except polaris code.", polaris_code == check_polaris_code)
        self.assert_("Fail! No return except polaris amount.", return_service_total == check_total)
        self.assert_("Fail! No return except polaris service size.", return_service_size == check_size)

        return_services = rsp.json().get("services", None)
        services_names = [srv["name"] for srv in return_services]
        self.assert_("Fail! No return except polaris service.", services_names == check_service_names)

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
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.service_name = "AutoTestPolarisService-" + _random_str
        self.start_step(
            "Create one regular polaris service: %s in namespace: %s." % (self.service_name, self.namespace_name))

        business = "AutoTestBusiness-" + _random_str
        department = "AutoTestDepartment-" + _random_str
        metadata_key = "AutoTestMetadataKey"
        metadata_value = "AutoTestMetadataValue-" + _random_str
        metadata = {metadata_key: metadata_value}
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        self.create_service_url = "http://" + self.polaris_console_addr + PolarisServer.SERVICE_PATH
        self.create_service_request = CreateServiceRequest(service_name=self.service_name,
                                                           namespace_name=self.namespace_name,
                                                           owners="polaris", business=business, department=department,
                                                           metadata=metadata,
                                                           comment="Auto test create polaris service %s" % now)
        rsp = self.polaris_server.create_service(self.create_service_url, self.create_service_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Create one regular polaris instance in service %s." % self.service_name)
        return_service_instance = self.create_single_service_instance(self.polaris_server, self.service_name,
                                                                      namespace_name=self.namespace_name)
        # ===========================
        self.start_step("Default describe services.")
        services = self.get_all_services(self.polaris_server, namespace_name=self.namespace_name)
        services_names = [srv["name"] for srv in services]
        _check_services_names = [self.service_name]
        if services_names:
            for srv_name in services_names:
                self.log_info("service %s wait for check." % _check_services_names)
                if _check_services_names:
                    if srv_name in _check_services_names:
                        self.log_info("Success to check return service %s!" % srv_name)
                        _check_services_names.remove(srv_name)
                    else:
                        self.log_info("No return except polaris service %s." % srv_name)
                else:
                    self.log_info("Success to check all services!")
                    break
        else:
            self.fail("Fail! No return except polaris services.")

        # ===========================
        self.start_step("Check describe service by correct service name.")
        _kwargs = {"url": self.describe_service_url, "service_name": self.service_name, "limit": 10, "offset": 0}
        self.check_return_service(check_total=1, check_size=1, check_polaris_code=200000,
                                  check_service_names=[self.service_name], **_kwargs)

        # ===========================
        self.start_step("Check describe service by correct service name and namespace name.")
        _kwargs.update({"namespace_name": self.namespace_name})
        self.check_return_service(check_total=1, check_size=1, check_polaris_code=200000,
                                  check_service_names=[self.service_name], **_kwargs)

        # ===========================
        self.start_step("Check describe service by correct service name, namespace name and business.")
        _kwargs.update({"business": business})
        self.check_return_service(check_total=1, check_size=1, check_polaris_code=200000,
                                  check_service_names=[self.service_name], **_kwargs)

        # ===========================
        self.start_step("Check describe service by correct service name, namespace name, business and department.")
        _kwargs.update({"department": department})
        self.check_return_service(check_total=1, check_size=1, check_polaris_code=200000,
                                  check_service_names=[self.service_name], **_kwargs)

        # ===========================
        self.start_step(
            "Check describe service by correct service name, namespace name, business, department, and host.")
        _kwargs.update({"host": return_service_instance["host"]})
        self.check_return_service(check_total=1, check_size=1, check_polaris_code=200000,
                                  check_service_names=[self.service_name], **_kwargs)

        # ===========================
        self.start_step(
            "Check describe service by correct service name, namespace name, business, department, host and metadata.")
        _kwargs.update({"key": metadata_key, "value": metadata_value})
        self.check_return_service(check_total=1, check_size=1, check_polaris_code=200000,
                                  check_service_names=[self.service_name], **_kwargs)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name])


if __name__ == '__main__':
    ServiceDescribeCheck().debug_run()
