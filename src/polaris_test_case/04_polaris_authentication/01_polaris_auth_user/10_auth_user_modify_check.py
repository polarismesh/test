# -*- coding: utf-8 -*-
from testbase.testcase import TestCase
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from src.polaris_test_lib.polaris import PolarisServer


class AuthUserModifyCheck(PolarisTestCase):
    """
    Used to modify user info test.
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

        # ==================================
        self.start_step("Modify email and phone: expected success. ")
        self.modify_user_url = "http://" + self.polaris_console_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, "13611112222",
                                                   "polaris@tencent.com")
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)

        # ==================================
        self.start_step("Modify comment: : expected success.  ")
        self.modify_user_url = "http://" + self.polaris_console_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, "13611112222",
                                                   "polaris@tencent.com", "polaris comment")
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)

        # ==================================
        self.start_step("Modify email and phone: expected fail，the phone number is invalid. ")
        self.modify_user_url = "http://" + self.polaris_console_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, "136111",
                                                   "polaris@tencent.com")
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 400413)

        # ==================================
        self.start_step("Modify email and phone: expected fail，the email is invalid. ")
        self.modify_user_url = "http://" + self.polaris_console_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, "13611112222",
                                                   "polaris")
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 400414)


if __name__ == '__main__':
    AuthUserModifyCheck().debug_run()
