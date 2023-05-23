# -*- coding: utf-8 -*-
from testbase.testcase import TestCase
from src.polaris_test_lib.polaris_testcase import PolarisTestCase


class AuthUserGetTokenCheck(PolarisTestCase):
    """
    Used to get user token test.
    """
    owner = "saracpli"
    status = TestCase.EnumStatus.Design
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.get_console_token()
        if self.token is not None:
            self.log_info("Success! Return expected value.")
            self.assert_("Success! Return expected value.", self.token is not None)
        else:
            self.log_info("Fail! Return an unexpected value.")
            self.assert_("Fail! Return an unexpected value.", self.token is None)


if __name__ == '__main__':
    AuthUserGetTokenCheck().debug_run()
