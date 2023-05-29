# -*- coding: utf-8 -*-

from src.polaris_test_lib.polaris import PolarisServer
from src.polaris_test_lib.polaris_testcase import PolarisTestCase
from testbase.testcase import TestCase
from testbase.conf import settings
from testbase.datadrive import DataDrive


@DataDrive({
    "Regular": {
        "username": settings.POLARIS_SERVER_USERNAME,
        "password": settings.POLARIS_SERVER_PASSWORD,
        "owner": settings.POLARIS_SERVER_TOKEN_OWNER,
        "case_desc": "Using correct username and password to login."
    },
    "irregular": {
        "username": settings.POLARIS_SERVER_USERNAME,
        "password": settings.POLARIS_SERVER_PASSWORD + "error",
        "owner": settings.POLARIS_SERVER_TOKEN_OWNER,
        "case_desc": "Using correct username and error password to login."
    },
})

class AuthUserLoginCheck(PolarisTestCase):
    """
    Used to test Polaris initial user/password to get token.

    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        login_url = "http://" + self.polaris_server_http_restful_api_addr + PolarisServer.LOGIN_PATH
        # ===========================
        self.start_step(self.casedata["case_desc"])
        rsp = PolarisServer.get_initial_token(url=login_url, username=self.casedata["username"],
                                              password=self.casedata["password"], owner=self.casedata["owner"])
        login_resp = rsp.json().get("loginResponse", None)
        polaris_code = rsp.json().get("code", None)
        # ===========================
        self.start_step("Check return token and polaris code.")
        if "irregular" in self.casedataname:
            self.assert_("Fail! No return except login response.", login_resp is None)
            self.assert_("Fail! No return except polaris code.", polaris_code == 401001)
        elif "regular" in self.casedataname and login_resp is None:
            self.fail("No login response return!")
            return
        else:
            token = login_resp.get("token", None)
            self.assert_("Fail! No return except token.", token is not None)
            self.assert_("Fail! No return except polaris code.", polaris_code == 200000)

        if self.test_result.passed:
            self.log_info("Success to check return token and polaris code!")


if __name__ == '__main__':
    AuthUserLoginCheck().debug_run()
