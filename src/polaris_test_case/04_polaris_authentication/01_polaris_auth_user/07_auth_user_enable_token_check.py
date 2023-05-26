# -*- coding: utf-8 -*-
import random

from testbase.testcase import TestCase
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from src.polaris_test_lib.polaris import PolarisServer


class AuthUserEnableTokenCheck(PolarisTestCase):
    """
    Used to enable user token test.
    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Design
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)

        # ==================================
        self.start_step("Get user info")
        self.user_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        rsp = self.polaris_server.describe_users(self.user_url, self.user_id)
        self.subuser_id_list = []
        if rsp.json().get("code") == 200000:
            for user in rsp.json().get("users"):
                if "autotest_user" in user["name"]:
                    self.subuser_id_list.append(user["id"])

        # ===========================
        if len(self.subuser_id_list)<=0:
            return

        self.start_step("Enable subuser token.")
        self.log_info(random.choice(self.subuser_id_list))
        operate_user_token_url = "http://" + self.polaris_console_addr + PolarisServer.OPERATE_USER_TOKEN_PATH
        rsp = self.polaris_server.operate_user_token(operate_user_token_url, random.choice(self.subuser_id_list),
                                                     token_enable=True)
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)


if __name__ == '__main__':
    AuthUserEnableTokenCheck().debug_run()
