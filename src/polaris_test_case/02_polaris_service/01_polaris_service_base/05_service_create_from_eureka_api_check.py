import random
import string
import time

import os
os.system("pip3 install xmltodict")
import xmltodict
from testbase.conf import settings
from testbase.testcase import TestCase

from src.polaris_test_lib.common_lib import CommonLib
from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class ServiceCreateFromEurekaApiCheck(PolarisTestCase):
    """
    Used to test creating service from eureka.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.start_step("Register one regular service from eureka rest api.")
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.service_name = "AUTO-TEST-POLARIS-EUREKA-SERVICE-" + _random_str.upper()
        # ===========================
        self.start_step("Check eureka register service.")
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        eureka_service_url = "http://" + settings.POLARIS_SERVER_EUREKA_SERVICE_ADDR + PolarisServer.EUREKA_REGISTER_PATH

        host = "test.eureka.service"
        app = self.service_name
        ip = CommonLib._random_ip()
        vip = CommonLib._random_ip()
        secure_vip = CommonLib._random_ip()
        status = "UP"
        _port = random.randint(30000, 50000)
        port = {"$": _port, "@enabled": "true"}
        _secure_port = random.randint(30000, 50000)
        secure_port = {"$": _secure_port, "@enabled": "true"}
        home_page_url = "http://test.eureka.service:%s/" % _port
        status_page_url = "http://test.eureka.service:%s/info" % _port
        health_check_url = "http://test.eureka.service:%s/health" % _port
        data_center_info = {"name": "MyOwn", "@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo"}
        lease_info = {
            "durationInSecs": 120,
            "evictionTimestamp": int(time.time()),
            "lastRenewalTimestamp": int(time.time()),
            "registrationTimestamp": int(time.time()),
            "renewalIntervalInSecs": 3,
            "serviceUpTimestamp": int(time.time())
        }
        metadata = {
            "auto.test.polaris.eureka.service": "true",
            "NODE_GROUP_ID": "0",
            "PRODUCT_CODE": "DEFAULT",
            "PRODUCT_ENV_CODE": "DEFAULT",
            "SERVICE_VERSION_CODE": "DEFAULT",
            "VERSION": "0.1.0"
        }

        rsp = self.polaris_server.eureka_register_service(
            eureka_service_url, host=host, app=app, ip=ip, vip=vip, secure_vip=secure_vip, status=status,
            port=port, secure_port=secure_port, home_page_url=home_page_url, status_page_url=status_page_url,
            health_check_url=health_check_url, data_center_info=data_center_info, lease_info=lease_info,
            metadata=metadata)
        self.log_info(rsp)
        # ===========================
        self.start_step("Check create service from polaris api.")
        return_services = self.get_all_services(self.polaris_server)
        return_service_names = [srv["name"] for srv in return_services]
        self.assert_("Fail! No return except polaris service.", self.service_name.lower() in return_service_names)
        # ===========================
        self.start_step("Check create service from eureka api.")
        time.sleep(10)  # sleep 10 secs wait for eureka server sync
        rsp = self.polaris_server.eureka_describe_service(eureka_service_url, app=app)
        rsp_json = xmltodict.parse(rsp.content)
        print(rsp_json)
        self.assert_("Fail! No return except eureka service.",
                     self.service_name.upper() == rsp_json["application"]["name"])

    def post_test(self):
        self.clean_test_services(self.polaris_server, service_name=self.service_name)


if __name__ == '__main__':
    ServiceCreateFromEurekaApiCheck().debug_run()
