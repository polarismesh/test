# -*- coding: utf-8 -*-
from testbase.testcase import TestCase
from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class AuthUserModifyPasswordCheck(PolarisTestCase):
    """
    Used to test modify password test.
    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Design
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        self.get_console_token()
        self.polaris_server = PolarisServer(self.token, self.user_id)
        # ==================================
        self.start_step("Create user test.")
        self.user_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        self.log_info(self.user_url)
        self.user_info = [{"name": "test001", "comment": "auth autotest create user test001", "password": "123456",
                           "source": "Polaris"}]
        rsp = self.polaris_server.create_user(self.user_url, self.user_info)
        if rsp.json() is not None and rsp.json().get("size") > 0:
            self.log_info("Create user success! user_info = %s" % self.user_info)
            self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)
        else:
            self.log_info("Create user fail! user_info = %s" % self.user_info)

        # ==================================
        self.start_step("Get user test.")
        self.log_info(self.user_url)
        self.user_info = [{"name": "test001", "comment": "auth autotest create user test111", "password": "123456",
                           "source": "Polaris"}]
        rsp = self.polaris_server.describe_users(self.user_url, self.user_id)
        self.update_user_id = ''
        if rsp.json().get("code") == 200000:
            for user in rsp.json().get("users"):
                if user["name"] == "test001":
                    self.update_user_id = user["id"]

        # ==================================
        self.start_step("Modify user password test.")
        self.modify_user_password_url = "http://" + self.polaris_console_addr + PolarisServer.MODIFY_USER_PASSWORD_PATH
        self.new_password = "polaris"
        rsp = self.polaris_server.modify_user_password(self.modify_user_password_url, self.user_id, self.new_password)
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)

        # ==================================
        self.start_step("Modify user password test,new password is blank.")
        self.modify_user_password_url = "http://" + self.polaris_console_addr + PolarisServer.MODIFY_USER_PASSWORD_PATH
        rsp = self.polaris_server.modify_user_password(self.modify_user_password_url, self.user_id, "")
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 500000)

        # ==================================
        self.start_step("Delete exist user test.")
        self.log_info(self.update_user_id)
        self.delete_user_url = "http://" + self.polaris_console_addr + PolarisServer.DELETE_USER_PATH
        rsp = self.polaris_server.delete_user(self.delete_user_url, self.update_user_id)
        if rsp.json() is not None and rsp.json().get("size") > 0:
            self.log_info("Delete user success! user_id = %s" % self.update_user_id)
            self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)
        else:
            self.log_info("Delete user fail! user_id = %s" % self.update_user_id)


if __name__ == '__main__':
    AuthUserModifyPasswordCheck().debug_run()
