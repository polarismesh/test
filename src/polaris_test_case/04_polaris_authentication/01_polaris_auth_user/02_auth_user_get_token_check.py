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

if __name__ == '__main__':
    AuthUserGetTokenCheck().debug_run()
