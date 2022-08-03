import os

from testbase.conf import settings

from src.polaris_test_lib.polaris import POLARIS_SERVER
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class PolarisInitialLoginCheck(PolarisTestCase):
    """
    Used to test Polaris initial user/password to get token.

    """
    owner = "atom"
    status = PolarisTestCase.EnumStatus.Ready
    priority = PolarisTestCase.EnumPriority.Normal
    timeout = 5

    # Specify the configuration file location.
    os.environ["QTAF_SETTINGS_MODULE"] = "src.settings"
    LOGIN_PATH = '/core/v1/user/login'

    def run_test(self):
        # ===========================
        self.start_step("Get POLARIS_CONSOLE_ADDR configuration.")
        POLARIS_CONSOLE_ADDR = settings.get("POLARIS_CONSOLE_ADDR", None)
        if POLARIS_CONSOLE_ADDR is not None:
            self.log_info("POLARIS_CONSOLE_ADDR: %s" % POLARIS_CONSOLE_ADDR)
            url = "http://" + POLARIS_CONSOLE_ADDR + self.LOGIN_PATH

            # ===========================
            self.start_step("Using correct username and password to get token.")
            rsp = POLARIS_SERVER.get_initial_token(url=url, username="polaris", password="polaris")
            login_resp = rsp.json().get("loginResponse", None)
            if login_resp is None:
                self.fail("No login response return!")
                return
            token = login_resp.get("token", None)
            polaris_code = rsp.json().get("code", None)
            # ===========================
            self.start_step("Check return token and polaris code.")
            self.assert_("Fail! No return except polaris code.", polaris_code is not None and polaris_code == 200000)
            self.assert_("Fail! No return except token.", token is not None)
            if self.test_result.passed:
                self.log_info("Success to check return token and polaris code!")

            # ===========================
            self.start_step("Using correct username and error password to get token.")
            rsp = POLARIS_SERVER.get_initial_token(url=url, username="polaris", password="polaris-error")
            login_resp = rsp.json().get("loginResponse", None)
            polaris_code = rsp.json().get("code", None)
            # ===========================
            self.start_step("Check return token and polaris code.")
            self.assert_("Fail! No return except polaris code.", polaris_code is not None and polaris_code == 401001)
            self.assert_("Fail! No return except login response.", login_resp is None)
            if self.test_result.passed:
                self.log_info("Success to check return token and polaris code!")

        else:
            self.fail("Check your config file in [{config_dir}] and set POLARIS_CONSOLE_ADDR in [{config_dir}]."
                      .format(config_dir=os.environ["QTAF_SETTINGS_MODULE"]))


if __name__ == '__main__':
    PolarisInitialLoginCheck().debug_run()
