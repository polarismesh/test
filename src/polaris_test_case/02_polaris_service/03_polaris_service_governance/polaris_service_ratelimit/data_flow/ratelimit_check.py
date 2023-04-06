import os
import random
import string
import time

from testbase.conf import settings
from testbase.testcase import TestCase

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class RatelimitCheck(PolarisTestCase):
    """
    Used to test ratelimit rule.

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

        self.ratelimit_caller_port = random.randint(30000, 50000)
        self.ratelimit_callee1_port = random.randint(30000, 50000)
        self.ratelimit_callee2_port = random.randint(30000, 50000)
        # ===========================
        self.get_kona_jdk()
        self.get_spring_cloud_tencent_example()
        new_directory = self.create_temp_test_directory(temp_dir_suffix=_random_str, resource_name="kona-jdk")
        self.create_temp_test_directory(
            temp_dir_suffix=_random_str,
            resource_name="spring-cloud-tencent-demo/%s" % settings.POLARIS_TEST_SCT_EXAMPLE_VERSION,
            file_name="ratelimit-*.jar")
        # ===========================
        self.start_step(
            "Register by spring cloud tencent demo: ratelimit-callee/caller"
            "[https://github.com/Tencent/spring-cloud-tencent/tree/{version}/spring-cloud-tencent-examples/polaris-ratelimit-example].")
        reg_ip = settings.POLARIS_SERVER_ADDR
        srv_maps = {
            "RateLimitCallerService": [
                {"srv_port": self.discovery_caller_port,
                 "jar_name": "ratelimit-caller-service"}
            ],
            "RateLimitCalleeService": [
                {"srv_port": self.discovery_callee1_port,
                 "jar_name": "ratelimit-callee-service"},
                {"srv_port": self.discovery_callee2_port,
                 "jar_name": "ratelimit-callee-service"}
            ]
        }

        for srv, srv_info in srv_maps.items():
            self.log_info("Register spring cloud tencent %s example." % srv)
            for _srv in srv_info:
                _region_info = _srv["srv_region_info"].split(":")
                _srv_port = _srv["srv_port"]
                _srv_jar_name = _srv["jar_name"]
                date_now = time.strftime("%Y%m%d%H%M", time.localtime(int(time.time())))
                cmd_exe = "cd {temp_dir} && nohup TencentKona-{kona_jdk_version}*/bin/java " \
                          "-Dspring.application.name={srv_name} " \
                          "-Dspring.cloud.polaris.stat.enabled=true " \
                          "-Dspring.cloud.polaris.stat.pushgateway.enabled=true " \
                          "-Dspring.cloud.polaris.stat.pushgateway.address={polaris_ip}:9091 " \
                          "-Dspring.cloud.polaris.address=grpc://{polaris_ip}:8091 " \
                          "-Dserver.port={srv_port} " \
                          "-jar {jar_name}*.jar " \
                          ">{jar_name}.{srv_port}.{date}.log 2>&1 &".format(
                    zone=_region_info[0], region=_region_info[1], campus=_region_info[2],
                    temp_dir=new_directory, kona_jdk_version=settings.POLARIS_TEST_SCT_KONA_JDK_VERSION,
                    polaris_ip=reg_ip, srv_port=_srv_port, srv_name=srv, jar_name=_srv_jar_name, date=date_now
                )
                if os.system(cmd_exe) != 0:
                    raise RuntimeError("Exec cmd: %s error!" % cmd_exe)
                else:
                    self.log_info("Exec cmd: %s success!" % cmd_exe)
        # ==================================
        self.start_step("Wait 60s for service start up...")
        success_list = []
        start = time.time()
        while len(success_list) < 3 and time.time() - start < 60:
            for srv_port in [self.discovery_caller_port, self.discovery_callee1_port, self.discovery_callee2_port]:
                if srv_port in success_list:
                    continue

                cmd_wait = "netstat -npl | grep %s" % srv_port
                if os.system(cmd_wait) != 0:
                    self.log_info("%s start up waiting..." % srv_port)
                    time.sleep(5)
                else:
                    self.log_info("%s start up success!" % srv_port)
                    success_list.append(srv_port)

        if len(success_list) < 3:
            raise RuntimeError("Start up failed!")
        time.sleep(60)

    # def post_test(self):
    #     # ===========================
    #     self.start_step("Stop all reatelimit services")
    #     for p in [self.ratelimit_caller_port, self.ratelimit_callee1_port, self.ratelimit_callee2_port]:
    #         cmd_kill = "ps axu | grep TencentKona | grep %s |grep -v grep | awk '{print $2}' | xargs kill -9 " % p
    #         os.system(cmd_kill)
    #     # ===========================
    #     self.start_step("Clean all discovery services")
    #     self.clean_test_services(self.polaris_server, service_name="DiscoveryCallerService")
    #     self.clean_test_services(self.polaris_server, service_name="DiscoveryCalleeService")


if __name__ == '__main__':
    RatelimitCheck().debug_run()
