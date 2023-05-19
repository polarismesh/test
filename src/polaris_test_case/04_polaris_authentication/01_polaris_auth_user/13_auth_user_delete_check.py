# -*- coding: utf-8 -*-

from testbase.testcase import TestCase
from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class AuthUserDeleteCheck(PolarisTestCase):
    """
    Used to test delete user.

    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # Get token
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        # ==================================
        self.start_step("Create user test.")
        self.user_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        self.log_info(self.user_url)
        self.user_info = [{"name": "test001", "comment": "auth autotest create user test111", "password": "123456",
                           "source": "Polaris"}]
        rsp = self.polaris_server.create_user(self.user_url, self.token, self.user_id, self.user_info)

        # ==================================
        self.start_step("Get user test.")
        self.log_info(self.user_url)
        self.user_info = [{"name": "test001", "comment": "auth autotest create user test111", "password": "123456",
                           "source": "Polaris"}]
        rsp = self.polaris_server.describe_users(self.user_url, self.token, self.user_id)
        delete_id = ''
        if rsp.json().get("code") == 200000:
            for user in rsp.json().get("users"):
                if user["name"] == "test001":
                    delete_id = user["id"]

        # ==================================
        self.start_step("Delete user test.")
        self.delete_user_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_USER_PATH
        self.log_info(self.delete_user_url)
        rsp = self.polaris_server.delete_user(self.delete_user_url, self.token, self.user_id, delete_id)
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)

        if self.test_result.passed:
            self.log_info("Delete user success!")
        else:
            self.log_info("Delete user fail!")


if __name__ == '__main__':
    AuthUserDeleteCheck().debug_run()
