from testbase.conf import settings
from testbase.testcase import TestCase


class PolarisInitialLoginCheck(TestCase):
    """
    Used to test Polaris initial user/password to get token.

    """
    owner = "atom"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 5

    def run_test(self):
        # ===========================
        self.start_step("")
        POLARIS_SERVER_ADDR = settings.get("POLARIS_SERVER_ADDR", "127.0.0.1:8080")

        # ===========================
        self.log_info("hello")
