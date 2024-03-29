import os
import random
import string
import time

os.system("pip3 install xmltodict")
import xmltodict
from testbase.conf import settings
from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class NativeEurekaServiceCheck(PolarisTestCase):
    """
    Used to test native eureka services register and discovery.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        _random_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        self.eureka_provider_name = "AT-NATIVE-EUREKA-SRV-PROVIDER-" + _random_str.upper()
        self.eureka_consumer_name = "AT-NATIVE-EUREKA-SRV-CONSUMER-" + _random_str.upper()
        self.eureka_provider_port = random.randint(30000, 50000)
        self.eureka_consumer_port = random.randint(30000, 50000)
        new_directory = self.create_temp_test_directory(temp_dir_suffix=_random_str, resource_name="eureka-demo")
        # ===========================
        self.get_kona_jdk(kona_jdk_version=11)
        self.create_temp_test_directory(temp_dir_suffix=_random_str, resource_name="kona-jdk")
        # ===========================
        self.start_step(
            "Register by native eureka demo"
            "[https://github.com/polarismesh/examples/tree/main/servicediscovery/eureka/eureka-java].")
        reg_ip = settings.POLARIS_SERVER_EUREKA_SERVICE_ADDR
        eureka_service_url = "http://" + settings.POLARIS_SERVER_EUREKA_SERVICE_ADDR + PolarisServer.EUREKA_REGISTER_PATH

        srv_maps = {
            "consumer": [self.eureka_consumer_name, self.eureka_consumer_port],
            "provider": [self.eureka_provider_name, self.eureka_provider_port]
        }

        for srv, eureka_app_info in srv_maps.items():
            self.log_info("Register eureka native %s demo." % srv)
            date_now = time.strftime("%Y%m%d%H%M", time.localtime(int(time.time())))
            cmd_exe = "cd {temp_dir} && nohup TencentKona-11*/bin/java " \
                      "-Deureka.client.serviceUrl.defaultZone=http://{eureka_reg_ip}/eureka/ " \
                      "-Dserver.port={srv_port} " \
                      "-Dspring.application.name={eureka_app_name} " \
                      "-jar eureka-{srv_type}*.jar > eureka-{srv_type}-{srv_port}-{date}.log 2>&1 &".format(
                temp_dir=new_directory, eureka_reg_ip=reg_ip, srv_port=eureka_app_info[1],
                eureka_app_name=eureka_app_info[0], srv_type=srv, date=date_now
            )

            if os.system(cmd_exe) != 0:
                raise RuntimeError("Exec cmd: %s error!" % cmd_exe)
            else:
                self.log_info("Exec cmd: %s success!" % cmd_exe)
        # ==================================
        self.start_step("Wait 30s for service start up...")
        success_list = []
        start = time.time()
        while len(success_list) < 2 and time.time() - start < 60:
            for srv_name, srv_info in srv_maps.items():
                if srv_name in success_list:
                    continue

                cmd_wait = "netstat -npl | grep %s" % srv_info[1]
                if os.system(cmd_wait) != 0:
                    self.log_info("%s start up waiting..." % srv_name)
                    time.sleep(5)
                else:
                    self.log_info("%s start up success!" % srv_name)
                    success_list.append(srv_name)

        if len(success_list) < len(srv_maps):
            raise RuntimeError("Start up failed!")

        time.sleep(30)
        # ===========================
        self.start_step("Check create service from polaris api.")
        return_services = self.get_all_services(self.polaris_server)
        return_service_names = [srv["name"] for srv in return_services]
        check_service_names = [self.eureka_provider_name.lower(), self.eureka_consumer_name.lower()]

        self.assert_("Fail! No return except polaris service.",
                     set(check_service_names).issubset(set(return_service_names)))

        # ===========================
        self.start_step("Check create service from eureka api.")

        for srv in check_service_names:
            rsp = self.polaris_server.eureka_describe_service(eureka_service_url, app=srv.upper())
            rsp_json = xmltodict.parse(rsp.content)
            print(rsp_json)
            self.assert_("Fail! No return except eureka service.", srv.upper() == rsp_json["application"]["name"])

        # ===========================
        self.start_step("Request eureka consumer to check provider discovery.")

        cmd_curl = "curl -sv 'http://127.0.0.1:%s/echo?providerServiceName=%s&value=hellomyfriends'" % (
            self.eureka_consumer_port, self.eureka_provider_name)
        self.req_and_check(
            srv_res_check_map={"hellomyfriends": {"eureka_provider": 1}},
            cmd_req_line=cmd_curl, all_req_num=10
        )

    def post_test(self):
        # ===========================
        self.start_step("Stop all eureka services")
        for p in [self.eureka_provider_port, self.eureka_consumer_port]:
            cmd_kill = "ps axu | grep TencentKona | grep %s |grep -v grep | awk '{print $2}' | xargs kill -9 " % p
            os.system(cmd_kill)
        # ===========================
        self.start_step("Wait for 10s to clean eureka services.")
        time.sleep(10)
        self.clean_test_services(self.polaris_server, service_name=self.eureka_consumer_name.lower())
        self.clean_test_services(self.polaris_server, service_name=self.eureka_provider_name.lower())
