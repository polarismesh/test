import random
import string
import time

from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateServiceRequest, DeleteServiceRequest
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceDeleteCheck(PolarisTestCase):
    """
    Used to test delete service.

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
        self.start_step("Create two regular polaris services in namespace: default.")

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
            CreateServiceRequest(service_name=self.service_name1, namespace_name="default", owners="polaris",
                                 business=business, department=department, metadata=metadata,
                                 comment="Auto test create polaris service %s" % now),
            CreateServiceRequest(service_name=self.service_name2, namespace_name="default", owners="polaris",
                                 business=business, department=department, metadata=metadata,
                                 comment="Auto test create polaris service %s" % now)
        ]
        rsp = self.polaris_server.create_service(self.create_service_url, self.create_service_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Delete error polaris service.")
        delete_service_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.DELETE_SERVICE_PATH
        err_service_name = "AutoTestPolarisService-err" + _random_str
        delete_service_req = DeleteServiceRequest(namespace_name="default", service_name=err_service_name)
        rsp = self.polaris_server.delete_service(delete_service_url, delete_service_req)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Delete correct polaris service.")
        delete_service_reqs = [
            DeleteServiceRequest(namespace_name="default", service_name=self.service_name1),
            DeleteServiceRequest(namespace_name="default", service_name=self.service_name2)
        ]
        rsp = self.polaris_server.delete_service(delete_service_url, delete_service_reqs)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        # ===========================
        self.start_step("Describe all services to check delete result.")

        return_services = self.get_all_services(self.polaris_server)
        return_services_names = [srv["name"] for srv in return_services]
        self.assert_("Fail! Deleted polaris services still exist.", self.service_name1 not in return_services_names)
        self.assert_("Fail! Deleted polaris services still exist.", self.service_name2 not in return_services_names)


if __name__ == '__main__':
    ServiceDeleteCheck().debug_run()
