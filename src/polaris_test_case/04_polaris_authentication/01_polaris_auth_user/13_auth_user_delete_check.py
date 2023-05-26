# -*- coding: utf-8 -*-

from testbase.testcase import TestCase
from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from src.polaris_test_lib.common_lib import CommonLib


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
        self.user_info = [
            {"name": "autotest_user_%s" % CommonLib._random_num(), "comment": "auth autotest create user comment",
             "password": "123456", "source": "Polaris"}]
        rsp = self.polaris_server.create_user(self.user_url, self.user_info)
        if rsp.json() is not None and rsp.json().get("size") > 0:
            self.log_info("Create user success! user_info = %s" % self.user_info)
            self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)
        else:
            self.log_info("Create user fail! user_info = %s" % self.user_info)

        # ==================================
        self.start_step("Get user test.")
        rsp = self.polaris_server.describe_users(self.user_url, self.user_id)
        delete_id_list = []
        if rsp.json().get("code") == 200000:
            for user in rsp.json().get("users"):
                if "autotest_user" in user["name"]:
                    delete_id_list.append(user["id"])

        # ==================================
        for delete_id in delete_id_list:
            self.start_step("Delete all subuser test.")
            self.delete_user_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_USER_PATH
            rsp = self.polaris_server.delete_user(self.delete_user_url, delete_id)
            if rsp.json() is not None and rsp.json().get("size") > 0:
                self.log_info("Delete user success! user_id = %s" % delete_id)
                self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)
            else:
                self.log_info("Delete user fail! user_id = %s" % delete_id)
        else:
            self.log_info("Delete user fail! No available subuser was found.")


if __name__ == '__main__':
    AuthUserDeleteCheck().debug_run()
