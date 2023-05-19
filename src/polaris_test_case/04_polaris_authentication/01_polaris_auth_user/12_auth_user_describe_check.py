# -*- coding: utf-8 -*-
import random

from testbase.testcase import TestCase
from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class AuthUserDescribeCheck(PolarisTestCase):
    """
    Used to test delete user.
    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        # ==================================
        self.start_step("Get all user list.")
        self.log_info("user_id: %s" % self.user_id)
        self.describe_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        rsp = self.polaris_server.describe_users(self.describe_url, self.token, self.user_id, self.user_id)
        self.assert_("Success! Return except code.", rsp.json().get("code") == 200000)
        # find out sub users
        self.sub_user_id_list = []
        if rsp.json().get("users") is not None:
            for user in rsp.json().get("users"):
                if user["owner"] is not None and user["owner"] != "":
                    self.sub_user_id_list.append(user["id"])

        # ==================================
        self.start_step("Get main user info by user_id")
        self.describe_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        rsp = self.polaris_server.describe_users(self.describe_url, self.token, self.user_id, self.user_id,
                                                 get_by_id=True)
        self.assert_("Success! Return except code.", rsp.json().get("code") == 200000)

        # ==================================
        self.start_step("Get sub user info by user_id")
        self.describe_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        self.log_info(random.choice(self.sub_user_id_list))
        rsp = self.polaris_server.describe_users(self.describe_url, self.token, self.user_id,
                                                 random.choice(self.sub_user_id_list), get_by_id=True)
        self.assert_("Success! Return except code.", rsp.json().get("code") == 200000)


if __name__ == '__main__':
    AuthUserDescribeCheck().debug_run()
