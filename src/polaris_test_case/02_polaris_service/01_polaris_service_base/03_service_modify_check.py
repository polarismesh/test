import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateServiceRequest, ModifyServiceRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceModifyCheck(PolarisTestCase):
    """
    Used to test modify service.

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
        self.start_step("Create two regular polaris services in namespace: %s." % self.namespace_name)

        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.service_name1 = "AutoTestPolarisService-" + _random_str
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.service_name2 = "AutoTestPolarisService-" + _random_str
        business = "AutoTestBusiness-" + _random_str
        department = "AutoTestDepartment-" + _random_str
        metadata_key = "AutoTestMetadataKey"
        metadata_value = "AutoTestMetadataValue-" + _random_str
        metadata = {metadata_key: metadata_value}
        self.create_service_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.SERVICE_PATH
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

        self.create_service_request = [
            CreateServiceRequest(service_name=self.service_name1, namespace_name=self.namespace_name, owners="polaris",
                                 business=business, department=department, metadata=metadata,
                                 comment="Auto test create polaris service %s" % now),
            CreateServiceRequest(service_name=self.service_name2, namespace_name=self.namespace_name, owners="polaris",
                                 business=business, department=department, metadata=metadata,
                                 comment="Auto test create polaris service %s" % now)
        ]
        rsp = self.polaris_server.create_service(self.create_service_url, self.create_service_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Modify service %s." % self.service_name1)
        self.modify_service_url = self.create_service_url

        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        business = "AutoTestBusiness-" + _random_str
        department = "AutoTestDepartment-" + _random_str
        metadata_key = "AutoTestMetadataKey"
        metadata_value = "AutoTestMetadataValue-" + _random_str
        metadata = {metadata_key: metadata_value}
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test modify polaris service %s" % now

        self.modify_service_request = ModifyServiceRequest(service_name=self.service_name1,
                                                           namespace_name=self.namespace_name,
                                                           owners="polaris", business=business, department=department,
                                                           metadata=metadata, comment=comment)
        rsp = self.polaris_server.modify_service(self.modify_service_url, self.modify_service_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Check modify service result.")
        self.describe_service_url = self.create_service_url
        rsp = self.polaris_server.describe_service(url=self.describe_service_url, service_name=self.service_name1,
                                                   limit=10, offset=0)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        return_services = rsp.json().get("services", None)
        for srv in return_services:
            self.assert_("Fail! No return except polaris service.", srv["name"] == self.service_name1)
            self.assert_("Fail! No return except polaris service business.", srv["business"] == business)
            self.assert_("Fail! No return except polaris service department.", srv["department"] == department)
            self.assert_("Fail! No return except polaris service metadata.", srv["metadata"] == metadata)
            self.assert_("Fail! No return except polaris service comment.", srv["comment"] == comment)

        # ===========================
        self.start_step("Modify two services at the same time.")
        self.modify_service_url = self.create_service_url

        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        business = "AutoTestBusiness-" + _random_str
        department = "AutoTestDepartment-" + _random_str
        metadata_key = "AutoTestMetadataKey"
        metadata_value = "AutoTestMetadataValue-" + _random_str
        metadata = {metadata_key: metadata_value}
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        comment = "Auto test modify two polaris service %s" % now

        self.modify_service_request = [
            ModifyServiceRequest(service_name=self.service_name1, namespace_name=self.namespace_name, owners="polaris",
                                 business=business, department=department, metadata=metadata, comment=comment),
            ModifyServiceRequest(service_name=self.service_name2, namespace_name=self.namespace_name, owners="polaris",
                                 business=business, department=department, metadata=metadata, comment=comment)
        ]
        rsp = self.polaris_server.modify_service(self.modify_service_url, self.modify_service_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Check modify service result.")
        self.describe_service_url = self.create_service_url
        for srv_name in [self.service_name1, self.service_name2]:
            rsp = self.polaris_server.describe_service(url=self.describe_service_url, service_name=srv_name,
                                                       limit=10, offset=0)

            polaris_code = rsp.json().get("code", None)
            self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

            return_services = rsp.json().get("services", None)
            for srv in return_services:
                self.assert_("Fail! No return except polaris service.", srv["name"] == srv_name)
                self.assert_("Fail! No return except polaris service business.", srv["business"] == business)
                self.assert_("Fail! No return except polaris service department.", srv["department"] == department)
                self.assert_("Fail! No return except polaris service metadata.", srv["metadata"] == metadata)
                self.assert_("Fail! No return except polaris service comment.", srv["comment"] == comment)

    def post_test(self):
        self.clean_test_namespaces(self.polaris_server, [self.namespace_name])


if __name__ == '__main__':
    ServiceModifyCheck().debug_run()
