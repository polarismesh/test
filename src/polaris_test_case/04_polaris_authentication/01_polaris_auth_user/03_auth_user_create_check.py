# -*- coding: utf-8 -*-

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from testbase.testcase import TestCase
from testbase import datadrive
from src.polaris_test_lib.common_lib import CommonLib

testdata = ({
    "USER_01": {
        "userinfo": [
            {"name": "autotest_user_%s" % CommonLib._random_num(), "comment": "auth autotest create user comment",
             "password": "123456", "source": "Polaris"}],
        "expect_code": 200000,
        "expect_info": "execute success"
    },
    "USER_02": {
        "userinfo": [
            {"name": "autotest_user_%s" % CommonLib._random_num(), "comment": "auth autotest create user comment",
             "password": "123456", "source": "Polaris"}],
        "expect_code": 200000,
        "expect_info": "execute success"
    },
    "USER_03": {
        "userinfo": [{"name": "", "comment": "auth autotest create user comment", "password": "123456",
                      "source": "Polaris"}],
        "expect_code": 400101,
        "expect_info": "invalid user name"
    },
    "USER_04": {
        "userinfo": [
            {"name": "autotest_user_%s" % CommonLib._random_num(), "comment": "auth autotest create user comment",
             "password": "", "source": "Polaris"}],
        "expect_code": 400412,
        "expect_info": "invalid user password"
    }
})


@datadrive.DataDrive(testdata)
class AuthUserCreateCheck(PolarisTestCase):
    """
    Used to test create user.
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
        self.create_user_url = "http://" + self.polaris_console_addr + PolarisServer.USER_PATH
        rsp = self.polaris_server.create_user(self.create_user_url, self.casedata["userinfo"])
        if rsp.json() is not None and rsp.json().get("size") > 0:
            self.log_info("Create user success! user_info = %s" % self.casedata["expect_info"])
            self.assert_("Success! Return except polaris code.", rsp.json().get("code") == self.casedata["expect_code"])
            self.assert_("Success! Return except login response.",
                         rsp.json().get("info") == self.casedata["expect_info"])
        else:
            self.log_info("Create user fail! user_info = %s" % self.casedata["expect_info"])


if __name__ == '__main__':
    AuthUserCreateCheck().debug_run()
