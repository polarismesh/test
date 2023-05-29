# -*- coding: utf-8 -*-
from testbase.testcase import TestCase
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.common_lib import CommonLib


class AuthUserModifyCheck(PolarisTestCase):
    """
    Used to modify user info test.
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
        self.start_step("Modify email and phone: expected success. ")
        self.modify_user_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, CommonLib._random_phone_num(),
                                                   CommonLib._random_email())
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)

        # ==================================
        self.start_step("Modify comment: : expected success.  ")
        self.modify_user_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, CommonLib._random_phone_num(),
                                                   CommonLib._random_email(), "polaris comment")
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 200000)

        # ==================================
        self.start_step("Modify email and phone: expected fail，the phone number is invalid. ")
        self.modify_user_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, '136111',
                                                   CommonLib._random_email())
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 400413)

        # ==================================
        self.start_step("Modify email and phone: expected fail，the email is invalid. ")
        self.modify_user_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.DESCRIBE_USER_PATH
        rsp = self.polaris_server.modify_user_info(self.modify_user_url, self.user_id, CommonLib._random_phone_num(),
                                                   "polaris_test")
        self.assert_("Success! Return except polaris code.", rsp.json().get("code") == 400414)


if __name__ == '__main__':
    AuthUserModifyCheck().debug_run()
