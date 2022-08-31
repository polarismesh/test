import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateServiceRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceCreateCheck(PolarisTestCase):
    """
    Used to test creating service.

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
        self.namespace_name = "default"
        self.service_name = "AutoTestPolarisService"
        business = "AutoTestBusiness"
        department = "AutoTestDepartment"
        metadata = {"AutoTestMetadataKey": "AutoTestMetadataValue"}
        self.start_step(
            "Create one regular polaris service: %s in namespace: %s." % (self.service_name, self.namespace_name))
        self.create_service_url = "http://" + self.polaris_console_addr + PolarisServer.SERVICE_PATH
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        self.create_service_request = CreateServiceRequest(service_name=self.service_name,
                                                           namespace_name=self.namespace_name,
                                                           owners="polaris", business=business, department=department,
                                                           metadata=metadata,
                                                           comment="Auto test create polaris service %s" % now)
        rsp = self.polaris_server.create_service(self.create_service_url, self.create_service_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_service = rsp.json()["responses"][0].get("service", None)
        if return_service is None:
            self.fail("Fail! No return except polaris service.")
        else:
            re_service_name = return_service.get("name", None)
            re_service_namespace_name = return_service.get("namespace", None)
            self.assert_("Fail! No return except polaris service name.", re_service_name == self.service_name)
            self.assert_("Fail! No return except polaris service namespace name.",
                         re_service_namespace_name == self.namespace_name)

        if self.test_result.passed:
            self.log_info("Success to check return service and polaris code!")

        services = self.get_all_services(self.polaris_server)
        for service in services:
            if service["name"] == self.service_name:
                self.assert_("Fail! No return except polaris service namespace.",
                             service["namespace"] == self.namespace_name)
                self.assert_("Fail! No return except polaris service business.", service["business"] == business)
                self.assert_("Fail! No return except polaris service department.",
                             service["department"] == department)
                self.assert_("Fail! No return except polaris service metadata.", service["metadata"] == metadata)
                self.assert_("Fail! No return except polaris service owners.", service["owners"] == self.user_id)
                break
        else:
            self.fail("Fail! No return except polaris service.")

        if self.test_result.passed:
            self.log_info("Success to check return service and polaris code!")

        # ===========================
        self.start_step("Bath Create two regular polaris services.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test create polaris service %s" % now
        self.service_name2 = "AutoTestPolarisService2"
        self.service_name3 = "AutoTestPolarisService3"
        create_service_request_list = []

        batch_create_service_names = [self.service_name2, self.service_name3]
        for n in batch_create_service_names:
            create_service_request_list.append(CreateServiceRequest(service_name=n, namespace_name=self.namespace_name,
                                                                    owners="polaris", comment=comment))

        rsp = self.polaris_server.create_service(self.create_service_url, create_service_request_list)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        _check_srv_names = batch_create_service_names.copy()
        for res in rsp.json()["responses"]:
            self.log_info("service %s wait for check." % _check_srv_names)
            return_services = res.get("service", None)
            if return_services is None:
                self.fail("Fail! No return except polaris services.")
            else:
                re_service_name = return_services.get("name", None)
                re_service_namespace_name = return_services.get("namespace", None)
                self.assert_("Fail! No return except polaris service name.", re_service_name in _check_srv_names)
                self.assert_("Fail! No return except polaris service namespace.",
                             re_service_namespace_name == self.namespace_name)
                if self.test_result.passed:
                    self.log_info("Success to check return service %s!" % re_service_name)
                    _check_srv_names.remove(re_service_name)

        # ===========================
        self.start_step("Create one repeat polaris service.")
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        self.create_service_request.comment = "Auto test create polaris namespace %s" % now
        rsp = self.polaris_server.create_service(self.create_service_url, self.create_service_request)
        polaris_code = rsp.json().get("code", None)
        re_polaris_info = rsp.json()["responses"][0].get("info", None)
        re_polaris_code = rsp.json()["responses"][0].get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code != 200000)
        self.assert_("Fail! No return except polaris code.", re_polaris_code == 400201)
        self.assert_("Fail! No return except polaris info.", "existed resource" in re_polaris_info)
        if self.test_result.passed:
            self.log_info("Success to check return token and polaris code!")

    def post_test(self):
        for srv in [self.service_name, self.service_name2, self.service_name3]:
            self.clean_test_services(self.polaris_server, namespace_name=self.namespace_name, service_name=srv)


if __name__ == '__main__':
    ServiceCreateCheck().debug_run()
