# -*- coding: utf-8 -*-
import random
import time

from testbase.testcase import TestCase
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from src.polaris_test_lib.polaris import PolarisServer


class AuthUserDisableTokenCheck(PolarisTestCase):
    """
    Used to disable user token test.
    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        # ==================================
        self.start_step("Get user")
        self.user_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        rsp = self.polaris_server.describe_users(self.user_url, self.user_id)
        self.subuser_id_list = []
        self.subuser_name_list = []
        if rsp.json().get("code") == 200000:
            for user in rsp.json().get("users"):
                if "autotest_user" in user["name"]:
                    self.subuser_id_list.append(user["id"])
                    self.subuser_name_list.append(user["name"])
        # ===========================
        self.start_step("Disable: The primary user token cannot be disabled.")
        self.operate_user_token_url = "http://" + self.polaris_console_addr + PolarisServer.OPERATE_USER_TOKEN_PATH
        rsp = self.polaris_server.operate_user_token(self.operate_user_token_url, self.user_id, token_enable=False)
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 401001)

        # ===========================
        if len(self.subuser_id_list) <= 0 or len(self.subuser_name_list) <= 0:
            return

        self.start_step("Disable: The subuser token can be disabled.")
        rsp = self.polaris_server.operate_user_token(self.operate_user_token_url, self.subuser_id_list[0],
                                                     token_enable=False)
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)
        time.sleep(5)

        # ===========================
        self.start_step("Disable: After the token of the subuser is disabled, access to the subuser fails.")
        # Login by subuser, get subuser token
        login_url = "http://" + self.polaris_console_addr + PolarisServer.LOGIN_PATH
        rsp = self.get_console_token(username=self.subuser_name_list[0], password='123456', owner='polaris')
        self.polaris_server.__init__(self.token, self.user_id)
        rsp = self.polaris_server.operate_user_token(self.operate_user_token_url, self.subuser_id_list[0])
        # token already disabled
        self.assert_("Success! Return except polaris code,", rsp.json().get("code") == 401003)

if __name__ == '__main__':
    AuthUserDisableTokenCheck().debug_run()
