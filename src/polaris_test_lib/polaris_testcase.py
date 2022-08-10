import os

from testbase import TestCase
from testbase.conf import settings

from src.polaris_test_lib.polaris import PolarisServer


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

    def get_console_token_first(self, username="polaris", password="polaris"):
        # ===========================
        self.start_step("Get polaris main user console token.")
        login_url = "http://" + self.polaris_console_addr + PolarisServer.LOGIN_PATH
        rsp = PolarisServer.get_initial_token(url=login_url, username=username, password=password)
        self.token = rsp.json().get("loginResponse", None).get("token", None)
        self.user_id = rsp.json().get("loginResponse", None).get("user_id", None)
