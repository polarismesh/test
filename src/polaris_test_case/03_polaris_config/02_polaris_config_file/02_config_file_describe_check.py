from testbase.conf import settings
from testbase.testcase import TestCase


class ServiceDescribeCheck(TestCase):
    """
    Used to test multiple or single service information acquisition.

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
