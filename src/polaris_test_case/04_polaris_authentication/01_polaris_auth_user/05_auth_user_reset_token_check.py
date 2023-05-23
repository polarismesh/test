# -*- coding: utf-8 -*-
from testbase.testcase import TestCase
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from src.polaris_test_lib.polaris import PolarisServer
import time


class AuthUserResetTokenCheck(PolarisTestCase):
    """
    Used to reset user token test.
    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Design
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        if self.token is not None:
            self.log_info("Success! Return expected value.")
            self.assert_("Success! Return expected value.", self.token is not None)
        else:
            self.log_info("Fail! Return an unexpected value.")
            self.assert_("Fail! Return an unexpected value.", self.token is None)

        # ===========================
        self.start_step("View user token")
        self.view_user_token_url = "http://" + self.polaris_console_addr + PolarisServer.VIEW_USER_TOKEN_PATH
        rsp = self.polaris_server.view_user_token(self.view_user_token_url, self.user_id)
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)

        # ===========================
        self.start_step("Reset user token")
        self.refresh_user_token_url = "http://" + self.polaris_console_addr + PolarisServer.REFRESH_USER_TOKEN_PATH
        rsp = self.polaris_server.refresh_user_token(self.refresh_user_token_url, self.user_id)
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)
        refresh_token = rsp.json().get("user")["auth_token"]
        time.sleep(3)

        self.start_step("Check：After the user token is reset, the old token becomes unavailable")
        self.describe_user_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        rsp = self.polaris_server.describe_users(self.describe_user_url, self.user_id)
        if rsp.json().get("code") == 407:
            self.log_info("Success! Return except polaris code.")
        else:
            self.log_info("Fail! Return unexcept polaris code:%s" % rsp.json().get("code"))
        self.assert_("Success! Get user info failed.", rsp.json().get("code") == 407)

        self.start_step("Check：After the token is reset, the user needs to log in again")
        # After the token is reset,renew token
        self.polaris_server.__init__(refresh_token, self.user_id)
        rsp = self.polaris_server.describe_users(self.describe_user_url, self.user_id)
        self.assert_("Success! Get user info failed.", rsp.json().get("code") == 200000)
        self.log_info("Success! Return except polaris code.")

if __name__ == '__main__':
    AuthUserResetTokenCheck().debug_run()
