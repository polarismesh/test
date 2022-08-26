import os
import time

from testbase import TestCase
from testbase.conf import settings

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_request import CreateNamespaceRequest, DeleteNamespaceRequest, \
    DeleteServiceInstanceRequest, DeleteServiceRequest


class PolarisTestCase(TestCase):
    # Specify the configuration file location.
    os.environ["QTAF_SETTINGS_MODULE"] = "src.settings"

    def pre_test(self):
        # ===========================
        self.start_step("Get POLARIS_CONSOLE_ADDR configuration.")
        POLARIS_CONSOLE_ADDR = settings.get("POLARIS_CONSOLE_ADDR", None)
        if POLARIS_CONSOLE_ADDR is not None:
            self.log_info("POLARIS_CONSOLE_ADDR: %s" % POLARIS_CONSOLE_ADDR)
            self.polaris_console_addr = POLARIS_CONSOLE_ADDR
        else:
            self.fail("Check your config file in [{config_dir}] and set POLARIS_CONSOLE_ADDR in [{config_dir}]."
                      .format(config_dir=os.environ["QTAF_SETTINGS_MODULE"]))

    def run_test(self):
        pass

    def get_console_token(self, username="polaris", password="polaris"):
        # ===========================
        self.start_step("Get polaris main user console token.")
        login_url = "http://" + self.polaris_console_addr + PolarisServer.LOGIN_PATH
        rsp = PolarisServer.get_initial_token(url=login_url, username=username, password=password)
        self.token = rsp.json().get("loginResponse", None).get("token", None)
        self.user_id = rsp.json().get("loginResponse", None).get("user_id", None)

    def create_single_namespace(self, polaris_server, namespace_name=None):
        # ===========================
        self.start_step("Create one regular polaris namespace.")
        self.create_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.NAMESPACE_PATH
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        self.create_namespace_request = CreateNamespaceRequest(namespace_name=namespace_name,
                                                               comment="Auto test create polaris namespace %s" % now)
        rsp = polaris_server.create_namespace(self.create_namespace_url, self.create_namespace_request)

        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_namespace = rsp.json()["responses"][0].get("namespace", None)
        if return_namespace is None:
            self.fail("Fail! No return except polaris namespace.")
            return
        else:
            re_namespace_name = return_namespace.get("name", None)
            self.assert_("Fail! No return except polaris namespace name.", re_namespace_name == namespace_name)

        if self.test_result.passed:
            self.log_info("Success to check return namespace and polaris code!")

    def clean_test_service_instances(self, polaris_server, namespace_name, service_name, wait_time=300):
        # ===========================
        self.start_step("Clean the test polaris service[%s:%s] instances." % (namespace_name, service_name))
        describe_service_instance_url = "http://" + self.polaris_console_addr + PolarisServer.INSTANCE_PATH

        now = time.time()
        while time.time() - now < wait_time:
            rsp = polaris_server.describe_service_instance(describe_service_instance_url, limit=10, offset=0,
                                                           namespace_name=namespace_name, service_name=service_name)
            instances = rsp.json().get("instances", None)
            if len(instances) == 0:
                self.log_info("Delete service instance finish.")
                return True

            delete_instance_requests = []
            for ins in instances:
                self.log_info("Delete service instance: %s:%s" % (ins["host"], ins["port"]))
                delete_instance_requests.append(DeleteServiceInstanceRequest(service_instance_id=ins["id"]))
            delete_service_instance_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_INSTANCE_PATH
            rsp = polaris_server.delete_service_instance(delete_service_instance_url, delete_instance_requests)
            polaris_code = rsp.json().get("code", None)
            if polaris_code != 200000:
                self.fail("Fail! No return except polaris code.")
                return False
            time.sleep(1)
        else:
            self.fail("Fail! Delete service instance time out.")
            return False

    def clean_test_services(self, polaris_server, namespace_name=None, service_name=None, wait_time=300):
        # ===========================
        self.start_step("Clean the test polaris services.")
        delete_service_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_SERVICE_PATH
        if all([namespace_name, service_name]):
            # ===========================
            self.start_step("Check service instances, delete first.")
            success = self.clean_test_service_instances(polaris_server, namespace_name=namespace_name,
                                                        service_name=service_name)
            if not success:
                self.fail("Fail to delete service: %s instances." % service_name)
                return False
            # ===========================
            self.start_step("Delete service: %s from namespace: %s" % (namespace_name, service_name))
            delete_service_req = DeleteServiceRequest(namespace_name=namespace_name, service_name=service_name)
            rsp = polaris_server.delete_service(delete_service_url, delete_service_req)
            polaris_code = rsp.json().get("code", None)
            if polaris_code != 200000:
                self.fail("Fail! No return except polaris code.")
                return False

        elif any([service_name, namespace_name]):
            service_name = service_name if service_name is not None else "all"
            namespace_name = namespace_name if namespace_name is not None else "all"
            # ===========================
            self.start_step("Delete %s service from %s namespace" % (service_name, namespace_name))
            describe_service_url = "http://" + self.polaris_console_addr + PolarisServer.SERVICE_PATH
            now = time.time()
            while time.time() - now < wait_time:
                rsp = polaris_server.describe_service(describe_service_url, limit=10, offset=0,
                                                      service_name=service_name, namespace_name=namespace_name)
                services = rsp.json().get("services", None)
                if len(services) == 0:
                    self.log_info("Delete service finish.")
                    break

                delete_service_requests = []
                for srv in services:
                    self.log_info("Delete service: %s from namespace: %s" % (srv["namespace"], srv["name"]))
                    # ===========================
                    self.start_step("Check service instances, delete first.")
                    success = self.clean_test_service_instances(polaris_server, namespace_name=srv["namespace"],
                                                                service_name=srv["name"])
                    if not success:
                        self.fail("Fail to delete service: %s instances." % srv["name"])
                        return False

                    delete_service_req = DeleteServiceRequest(namespace_name=namespace_name, service_name=service_name)
                    delete_service_requests.append(delete_service_req)

                rsp = polaris_server.delete_service(delete_service_url, delete_service_requests)
                polaris_code = rsp.json().get("code", None)
                if polaris_code != 200000:
                    self.fail("Fail! No return except polaris code.")
                    return False
                time.sleep(1)
            else:
                self.fail("Fail! Delete service time out.")
                return False

        else:
            raise Exception("You must assign at least namespace_name or service_name")

    def clean_test_namespaces(self, polaris_server, namespace_names):
        # ===========================
        self.start_step("Clean the test polaris namespaces.")
        delete_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_NAMESPACE_PATH

        delete_namespace_requests = []
        for n in namespace_names:
            self.log_info("Delete namespace: %s" % n)
            # ===========================
            self.start_step("Check services, delete first.")
            success = self.clean_test_services(polaris_server, namespace_name=n)
            if not success:
                self.fail("Fail to delete services from namespace: %s." % n)
                return False

            delete_namespace_requests.append(DeleteNamespaceRequest(namespace_name=n))
        rsp = polaris_server.delete_namespace(delete_namespace_url, delete_namespace_requests)
        polaris_code = rsp.json().get("code", None)
        if polaris_code != 200000:
            self.fail("Fail! No return except polaris code.")
            return False
        return True

    def get_all_namespaces(self, polaris_server, limit=10):
        self.describe_namespace_url = "http://" + self.polaris_console_addr + PolarisServer.NAMESPACE_PATH
        rsp = polaris_server.describe_namespace(self.describe_namespace_url, limit=limit, offset=0)
        polaris_code = rsp.json().get("code", None)
        self.assert_("Fail! No return except polaris code.", polaris_code == 200000)
        return_namespace_total = rsp.json().get("amount", None)

        return_namespaces = []
        if return_namespace_total > limit:
            self.log_info("requery with the total number of Polaris namespaces.")
            query_times = (return_namespace_total / limit) + 1
            for offset in range(query_times):
                rsp = polaris_server.describe_namespace(self.describe_namespace_url,
                                                        limit=return_namespace_total, offset=offset)
                polaris_code = rsp.json().get("code", None)
                self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

                return_namespaces += rsp.json().get("namespaces", None)
        else:
            return_namespaces = rsp.json().get("namespaces", None)
        return return_namespaces
